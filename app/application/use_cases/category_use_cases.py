"""Category use cases."""

from uuid import UUID
from typing import List

from app.domain.entities import Category
from app.domain.ports import CategoryRepository
from app.domain.exceptions import EntityNotFoundError
from app.application.dtos import (
    CategoryDTO, CreateCategoryRequest, UpdateCategoryRequest
)
from app.application.mappers import CategoryMapper


class GetCategoryUseCase:
    """Use case for getting a category by ID."""

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: UUID) -> CategoryDTO:
        """Get category by ID."""
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise EntityNotFoundError(f"Category {category_id} not found")
        return CategoryMapper.to_dto(category)


class ListCategoriesUseCase:
    """Use case for listing all categories."""

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, skip: int = 0, limit: int = 10) -> List[CategoryDTO]:
        """Get all categories."""
        categories = await self.repository.get_all(skip, limit)
        return [CategoryMapper.to_dto(c) for c in categories]


class CreateCategoryUseCase:
    """Use case for creating a category."""

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, request: CreateCategoryRequest) -> CategoryDTO:
        """Create a new category."""
        category = Category(
            name=request.name,
            description=request.description
        )
        saved = await self.repository.add(category)
        return CategoryMapper.to_dto(saved)


class UpdateCategoryUseCase:
    """Use case for updating a category."""

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: UUID, request: UpdateCategoryRequest) -> CategoryDTO:
        """Update a category."""
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise EntityNotFoundError(f"Category {category_id} not found")

        # Update fields
        if request.name:
            category.name = request.name
        if request.description:
            category.description = request.description
        if request.is_active is not None:
            category.is_active = request.is_active

        updated = await self.repository.update(category)
        return CategoryMapper.to_dto(updated)


class DeleteCategoryUseCase:
    """Use case for deleting a category."""

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: UUID) -> bool:
        """Delete a category."""
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise EntityNotFoundError(f"Category {category_id} not found")
        return await self.repository.delete(category_id)
