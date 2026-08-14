import os
import uuid
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import mimetypes

from app.models.project import Project
from app.models.repository import Repository
from app.models.document import Document, DocumentStatus
from app.services.storage_service import StorageService
from app.services.project_service import ProjectService

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".c", ".cpp", ".h", ".hpp",
    ".go", ".rs", ".rb", ".php", ".cs", ".kt", ".swift", ".sql", ".md", ".txt",
    ".json", ".yaml", ".yml", ".toml", ".xml", ".html", ".css"
}

IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", "venv", ".venv", "env", "build", "dist", ".idea", ".vscode"
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB for MVP

class GithubService:
    @staticmethod
    def _validate_url(url: str) -> str:
        if not url.startswith("https://github.com/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only public https://github.com/ repositories are supported in this MVP."
            )
        # Strip trailing slashes and .git
        url = url.rstrip("/")
        if url.endswith(".git"):
            url = url[:-4]
        return url

    @staticmethod
    def _is_allowed_file(filepath: Path) -> bool:
        if any(ignored in filepath.parts for ignored in IGNORED_DIRS):
            return False

        # Also ignore hidden files/directories starting with '.'
        if any(part.startswith('.') for part in filepath.parts if part != '.'):
            return False

        # Check size
        try:
            if filepath.stat().st_size > MAX_FILE_SIZE:
                return False
        except OSError:
            return False

        ext = filepath.suffix.lower()
        if ext in ALLOWED_EXTENSIONS:
            return True

        if filepath.name.lower() in ("readme", "readme.md", "readme.txt"):
            return True

        return False

    @staticmethod
    async def ingest_repository(
        db: AsyncSession,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        repository_url: str,
        branch: str = "main"
    ) -> Repository:
        # Enforce project ownership
        project = await ProjectService.get_project(db, project_id, user_id)

        # Validate URL
        safe_url = GithubService._validate_url(repository_url)

        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                # Clone shallowly
                process = subprocess.run(
                    ["git", "clone", "--depth", "1", "-b", branch, safe_url, tmp_dir],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone repository: {e.stderr}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to clone repository. Ensure it is public and the branch exists. Error: {e.stderr[:200]}"
                )

            # Get commit SHA
            try:
                sha_process = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=tmp_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )
                commit_sha = sha_process.stdout.strip()
            except subprocess.CalledProcessError:
                commit_sha = None

            # Create repository record
            repo = Repository(
                project_id=project_id,
                repository_url=safe_url,
                branch=branch,
                commit_sha=commit_sha
            )
            db.add(repo)
            await db.flush()  # To get the repo.id

            repo_path = Path(tmp_dir)
            documents = []

            # Walk and process files
            for root, _, files in os.walk(tmp_dir):
                for file_name in files:
                    file_path = Path(root) / file_name
                    if not GithubService._is_allowed_file(file_path):
                        continue

                    rel_path = str(file_path.relative_to(repo_path))

                    # Store file
                    stored_filename, storage_path, file_size, sha256_hash = StorageService.save_local_file(
                        str(file_path),
                        file_name
                    )

                    mime_type, _ = mimetypes.guess_type(file_name)
                    if not mime_type:
                        mime_type = "text/plain"

                    # Create document
                    doc = Document(
                        project_id=project_id,
                        title=rel_path,
                        original_filename=file_name,
                        stored_filename=stored_filename,
                        file_path=storage_path,
                        mime_type=mime_type,
                        file_size=file_size,
                        sha256_hash=sha256_hash,
                        status=DocumentStatus.UPLOADED,
                        source_type="github",
                        repository_id=repo.id,
                        repo_file_path=rel_path
                    )
                    documents.append(doc)

            db.add_all(documents)
            await db.commit()

            # Refresh repo to include relationships if needed, or just return it
            await db.refresh(repo)
            return repo
