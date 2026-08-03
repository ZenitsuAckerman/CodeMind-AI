from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.document import DocumentResponse
from app.schemas.search import SearchRequest, SearchResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.project_service import ProjectService
from app.services.document_service import DocumentService
from app.services.document_processing_service import DocumentProcessingService
from app.services.indexing_service import IndexingService
from app.services.retrieval_service import RetrievalService
from app.services.chat_service import ChatService
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new project.
    """
    return await ProjectService.create_project(db=db, project_in=project_in, user_id=current_user.id)

@router.get("/", response_model=List[ProjectResponse])
async def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all projects for the current user.
    """
    return await ProjectService.get_user_projects(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectResponse)
async def read_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific project by id.
    """
    return await ProjectService.get_project(db=db, project_id=project_id, user_id=current_user.id)

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a specific project.
    """
    return await ProjectService.update_project(db=db, project_id=project_id, project_in=project_in, user_id=current_user.id)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a specific project.
    """
    await ProjectService.delete_project(db=db, project_id=project_id, user_id=current_user.id)

@router.post("/{project_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    project_id: UUID,
    title: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a document to a specific project.
    """
    return await DocumentService.upload_document(db=db, project_id=project_id, user_id=current_user.id, title=title, file=file)

@router.get("/{project_id}/documents", response_model=List[DocumentResponse])
async def read_project_documents(
    project_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all documents for a specific project.
    """
    return await DocumentService.get_project_documents(db=db, project_id=project_id, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/{project_id}/documents/{document_id}/process", status_code=status.HTTP_202_ACCEPTED)
async def process_document(
    project_id: UUID,
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Extract raw text from a document in a specific project.
    """
    # Verify project ownership first implicitly through DocumentProcessingService getting the document
    await DocumentProcessingService.process_document(db=db, document_id=document_id, user_id=current_user.id)
    return {"message": "Document processing completed successfully"}

@router.post("/{project_id}/documents/{document_id}/index", status_code=status.HTTP_202_ACCEPTED)
async def index_document(
    project_id: UUID,
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Run the RAG indexing pipeline on a processed document (chunking, embedding, vector storage).
    """
    await IndexingService.index_document(db=db, document_id=document_id, user_id=current_user.id)
    return {"message": "Document indexing completed successfully"}

@router.post("/{project_id}/search", response_model=SearchResponse)
async def search_project(
    project_id: UUID,
    request: SearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Perform a semantic search against all indexed documents within a project.
    Returns the most relevant chunks without calling an LLM.
    """
    results = await RetrievalService.search(
        db=db, 
        project_id=project_id, 
        user_id=current_user.id, 
        query=request.query, 
        limit=request.limit
    )
    return SearchResponse(results=results)

@router.post("/{project_id}/chat", response_model=ChatResponse)
async def chat_with_project(
    project_id: UUID,
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Ask a natural language question about the project's documents.
    """
    return await ChatService.chat_with_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        question=request.question
    )
