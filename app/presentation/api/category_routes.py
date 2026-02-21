"""Category API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List

from app.domain.ports import CategoryRepository
from app.domain.exceptions import EntityNotFoundError, DomainException
from app.infrastructure.config import RepositoryContainer
from app.application.use_cases import (
    GetCategoryUseCase,
    ListCategoriesUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)
from app.application.dtos import CreateCategoryRequest, UpdateCategoryRequest
from app.presentation.schemas import (
    CategorySchema,
    CreateCategorySchema,
    UpdateCategorySchema
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(
    category_id: UUID,
    repo: CategoryRepository = Depends(RepositoryContainer.get_category_repository)
):
    """Get a category by ID."""
    try:
        use_case = GetCategoryUseCase(repo)
        dto = await use_case.execute(category_id)
        return {
            "id": dto.id,
            "name": dto.name,
            "description": dto.description,
            "is_active": dto.is_active,
            "created_at": dto.created_at,
            "updated_at": dto.updated_at
        }
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[CategorySchema])
async def list_categories(
    skip: int = 0,
    limit: int = 10,
    repo: CategoryRepository = Depends(RepositoryContainer.get_category_repository)
):
    """List all categories."""
    try:
        use_case = ListCategoriesUseCase(repo)
        dtos = await use_case.execute(skip, limit)
        return [
            {
                "id": dto.id,
                "name": dto.name,
                "description": dto.description,
                "is_active": dto.is_active,
                "created_at": dto.created_at,
                "updated_at": dto.updated_at
            }
            for dto in dtos
        ]
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(
    schema: CreateCategorySchema,
    repo: CategoryRepository = Depends(RepositoryContainer.get_category_repository)
):
    """Create a new category."""
    try:
        request = CreateCategoryRequest(name=schema.name, description=schema.description)
        use_case = CreateCategoryUseCase(repo)
        dto = await use_case.execute(request)
        return {
            "id": dto.id,
            "name": dto.name,
            "description": dto.description,
            "is_active": dto.is_active,
            "created_at": dto.created_at,
            "updated_at": dto.updated_at
        }
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: UUID,
    schema: UpdateCategorySchema,
    repo: CategoryRepository = Depends(RepositoryContainer.get_category_repository)
):
    """Update a category."""
    try:
        request = UpdateCategoryRequest(
            name=schema.name,
            description=schema.description,
            is_active=schema.is_active
        )
        use_case = UpdateCategoryUseCase(repo)
        dto = await use_case.execute(category_id, request)
        return {
            "id": dto.id,
            "name": dto.name,
            "description": dto.description,
            "is_active": dto.is_active,
            "created_at": dto.created_at,
            "updated_at": dto.updated_at
        }
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    repo: CategoryRepository = Depends(RepositoryContainer.get_category_repository)
):
    """Delete a category."""
    try:
        use_case = DeleteCategoryUseCase(repo)
        await use_case.execute(category_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
