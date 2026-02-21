"""
Guía de Extensión - Cómo Agregar Nuevas Entidades

Este archivo muestra cómo agregar una nueva entidad (Reviews) siguiendo
la arquitectura hexagonal.
"""

# ============================================================================

# PASO 1: DOMAIN LAYER - Crear la Entidad y el Puerto

# ============================================================================

# app/domain/entities/review.py

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal

from app.domain.value_objects import Money
from app.domain.exceptions import InvalidEntityError

@dataclass
class Review(BaseEntity):
"""Review entity."""
product_id: UUID
user_id: UUID
rating: float # 1-5
title: str
content: str
is_verified_purchase: bool = False

    def __post_init__(self):
        if not (1 <= self.rating <= 5):
            raise InvalidEntityError("Rating must be between 1 and 5")
        if not self.title or len(self.title) < 5:
            raise InvalidEntityError("Title must be at least 5 characters")
        if not self.content or len(self.content) < 10:
            raise InvalidEntityError("Content must be at least 10 characters")

# app/domain/ports/**init**.py (agregar)

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities import Review

class ReviewRepository(ABC):
"""Port for review persistence."""

    @abstractmethod
    async def add(self, review: Review) -> Review:
        """Add a new review."""
        pass

    @abstractmethod
    async def get_by_id(self, review_id: UUID) -> Optional[Review]:
        """Get review by ID."""
        pass

    @abstractmethod
    async def get_by_product_id(self, product_id: UUID, skip: int = 0, limit: int = 50) -> List[Review]:
        """Get reviews by product ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 50) -> List[Review]:
        """Get reviews by user ID."""
        pass

    @abstractmethod
    async def update(self, review: Review) -> Review:
        """Update a review."""
        pass

    @abstractmethod
    async def delete(self, review_id: UUID) -> bool:
        """Delete a review."""
        pass

# ============================================================================

# PASO 2: APPLICATION LAYER - DTOs y Use Cases

# ============================================================================

# app/application/dtos/**init**.py (agregar)

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class ReviewDTO:
"""Review data transfer object."""
id: UUID
product_id: UUID
user_id: UUID
rating: float
title: str
content: str
is_verified_purchase: bool
created_at: datetime
updated_at: datetime

@dataclass
class CreateReviewRequest:
"""Request to create a review."""
product_id: UUID
rating: float
title: str
content: str

# app/application/mappers/**init**.py (agregar)

from app.domain.entities import Review
from app.application.dtos import ReviewDTO

class ReviewMapper:
"""Mapper for Review entity."""

    @staticmethod
    def to_dto(entity: Review) -> ReviewDTO:
        """Convert review entity to DTO."""
        return ReviewDTO(
            id=entity.id,
            product_id=entity.product_id,
            user_id=entity.user_id,
            rating=entity.rating,
            title=entity.title,
            content=entity.content,
            is_verified_purchase=entity.is_verified_purchase,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

# app/application/use_cases/review_use_cases.py

from uuid import UUID
from typing import List

from app.domain.entities import Review
from app.domain.ports import ReviewRepository, ProductRepository, OrderRepository
from app.domain.exceptions import EntityNotFoundError, InvalidEntityError
from app.application.dtos import ReviewDTO, CreateReviewRequest
from app.application.mappers import ReviewMapper

class CreateReviewUseCase:
"""Use case for creating a review."""

    def __init__(
        self,
        review_repo: ReviewRepository,
        product_repo: ProductRepository,
        order_repo: OrderRepository
    ):
        self.review_repo = review_repo
        self.product_repo = product_repo
        self.order_repo = order_repo

    async def execute(self, user_id: UUID, request: CreateReviewRequest) -> ReviewDTO:
        """Create a new review."""
        # Verify product exists
        product = await self.product_repo.get_by_id(request.product_id)
        if not product:
            raise EntityNotFoundError(f"Product {request.product_id} not found")

        # Check if user purchased this product
        # (Implementación simplificada)
        is_verified = True  # Aquí iría lógica más compleja

        # Create review entity
        review = Review(
            product_id=request.product_id,
            user_id=user_id,
            rating=request.rating,
            title=request.title,
            content=request.content,
            is_verified_purchase=is_verified
        )

        saved = await self.review_repo.add(review)
        return ReviewMapper.to_dto(saved)

class GetProductReviewsUseCase:
"""Use case for getting product reviews."""

    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def execute(self, product_id: UUID, skip: int = 0, limit: int = 50) -> List[ReviewDTO]:
        """Get reviews for a product."""
        reviews = await self.repository.get_by_product_id(product_id, skip, limit)
        return [ReviewMapper.to_dto(r) for r in reviews]

# ============================================================================

# PASO 3: INFRASTRUCTURE LAYER - Implementación del Repositorio

# ============================================================================

# app/infrastructure/repositories/**init**.py (agregar)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID

from app.domain.entities import Review
from app.domain.ports import ReviewRepository

class SQLAlchemyReviewRepository(ReviewRepository):
"""Review repository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, review: Review) -> Review:
        """Add a new review."""
        self.session.add(review)
        await self.session.commit()
        await self.session.refresh(review)
        return review

    async def get_by_id(self, review_id: UUID) -> Optional[Review]:
        """Get review by ID."""
        stmt = select(Review).where(Review.id == review_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_product_id(self, product_id: UUID, skip: int = 0, limit: int = 50) -> List[Review]:
        """Get reviews by product ID."""
        stmt = select(Review).where(Review.product_id == product_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 50) -> List[Review]:
        """Get reviews by user ID."""
        stmt = select(Review).where(Review.user_id == user_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, review: Review) -> Review:
        """Update a review."""
        await self.session.merge(review)
        await self.session.commit()
        return review

    async def delete(self, review_id: UUID) -> bool:
        """Delete a review."""
        review = await self.get_by_id(review_id)
        if not review:
            return False
        await self.session.delete(review)
        await self.session.commit()
        return True

# app/infrastructure/config/**init**.py (agregar en RepositoryContainer)

@staticmethod
async def get_review_repository(
session: AsyncSession = Depends(get_db_session)
) -> ReviewRepository:
"""Get review repository instance."""
return SQLAlchemyReviewRepository(session)

# ============================================================================

# PASO 4: PRESENTATION LAYER - Routers y Schemas

# ============================================================================

# app/presentation/schemas/**init**.py (agregar)

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class ReviewSchema(BaseModel):
"""Review response schema."""
id: UUID
product_id: UUID
user_id: UUID
rating: float
title: str
content: str
is_verified_purchase: bool
created_at: datetime
updated_at: datetime

    class Config:
        from_attributes = True

class CreateReviewSchema(BaseModel):
"""Create review request schema."""
product_id: UUID
rating: float = Field(..., ge=1, le=5)
title: str = Field(..., min_length=5, max_length=200)
content: str = Field(..., min_length=10, max_length=2000)

# app/presentation/api/review_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List

from app.domain.ports import ReviewRepository
from app.domain.exceptions import EntityNotFoundError, DomainException
from app.infrastructure.config import RepositoryContainer
from app.application.use_cases import (
CreateReviewUseCase,
GetProductReviewsUseCase
)
from app.application.dtos import CreateReviewRequest
from app.presentation.schemas import ReviewSchema, CreateReviewSchema

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
schema: CreateReviewSchema,
user_id: UUID, # Desde auth
repo: ReviewRepository = Depends(RepositoryContainer.get_review_repository)
):
"""Create a new review."""
try:
request = CreateReviewRequest(
product_id=schema.product_id,
rating=schema.rating,
title=schema.title,
content=schema.content
)
use_case = CreateReviewUseCase(repo)
dto = await use_case.execute(user_id, request)
return {
"id": dto.id,
"product_id": dto.product_id,
"user_id": dto.user_id,
"rating": dto.rating,
"title": dto.title,
"content": dto.content,
"is_verified_purchase": dto.is_verified_purchase,
"created_at": dto.created_at,
"updated_at": dto.updated_at
}
except DomainException as e:
raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/product/{product_id}", response_model=List[ReviewSchema])
async def get_product_reviews(
product_id: UUID,
skip: int = 0,
limit: int = 50,
repo: ReviewRepository = Depends(RepositoryContainer.get_review_repository)
):
"""Get reviews for a product."""
use_case = GetProductReviewsUseCase(repo)
dtos = await use_case.execute(product_id, skip, limit)
return [
{
"id": dto.id,
"product_id": dto.product_id,
"user_id": dto.user_id,
"rating": dto.rating,
"title": dto.title,
"content": dto.content,
"is_verified_purchase": dto.is_verified_purchase,
"created_at": dto.created_at,
"updated_at": dto.updated_at
}
for dto in dtos
]

# app/presentation/api/**init**.py (agregar)

from app.presentation.api.review_routes import router as review_router

api_router.include_router(review_router)

# ============================================================================

# RESUMEN: 4 Pasos para Agregar una Nueva Entidad

# ============================================================================

"""

1. DOMAIN (sin dependencias externas):
    - Crear entidad (Review)
    - Crear puerto/interface (ReviewRepository)
    - Definir excepciones si es necesario

2. APPLICATION (orquestación):
    - Crear DTOs (ReviewDTO, CreateReviewRequest)
    - Crear mappers (ReviewMapper)
    - Crear use cases (CreateReviewUseCase, GetProductReviewsUseCase)

3. INFRASTRUCTURE (detalles técnicos):
    - Implementar repositorio (SQLAlchemyReviewRepository)
    - Agregar a contenedor de DI (RepositoryContainer)

4. PRESENTATION (interfaz):
    - Crear esquemas Pydantic (ReviewSchema, CreateReviewSchema)
    - Crear routers (review_routes.py)
    - Incluir en api_router

¡Todo sin modificar entidades existentes! (Open/Closed Principle)
"""
