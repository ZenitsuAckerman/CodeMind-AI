import os
import uuid
import hashlib
from pathlib import Path
from fastapi import UploadFile

STORAGE_DIR = Path("backend/storage/uploads")

class StorageService:
    @staticmethod
    def _ensure_storage_dir():
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    async def save_file(file: UploadFile) -> tuple[str, str, int, str]:
        """
        Saves a file to local storage.
        Returns a tuple of (stored_filename, file_path, file_size, sha256_hash).
        """
        StorageService._ensure_storage_dir()
        
        # Generate unique filename
        stored_filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        file_path = STORAGE_DIR / stored_filename
        
        # Save file chunks and calculate hash
        file_size = 0
        hasher = hashlib.sha256()
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                buffer.write(chunk)
                hasher.update(chunk)
                file_size += len(chunk)
        
        await file.seek(0)  # Reset pointer if needed later
        
        return stored_filename, str(file_path), file_size, hasher.hexdigest()

    @staticmethod
    def save_local_file(source_path: str, original_filename: str) -> tuple[str, str, int, str]:
        """
        Saves a local file to storage.
        Returns a tuple of (stored_filename, file_path, file_size, sha256_hash).
        """
        StorageService._ensure_storage_dir()

        # Generate unique filename
        stored_filename = f"{uuid.uuid4()}{os.path.splitext(original_filename)[1]}"
        file_path = STORAGE_DIR / stored_filename

        import shutil
        import hashlib

        # Save file chunks and calculate hash
        file_size = 0
        hasher = hashlib.sha256()
        with open(source_path, "rb") as source, open(file_path, "wb") as dest:
            while chunk := source.read(1024 * 1024):
                dest.write(chunk)
                hasher.update(chunk)
                file_size += len(chunk)

        return stored_filename, str(file_path), file_size, hasher.hexdigest()

    @staticmethod
    def delete_file(file_path: str) -> None:
        """
        Deletes a file from local storage if it exists.
        """
        path = Path(file_path)
        if path.exists() and path.is_file():
            os.remove(path)
