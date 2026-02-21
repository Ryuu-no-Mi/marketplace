"""Product API routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID
from typing import List

from app.domain.ports import CategoryRepository, ProductRepository
from app.domain.exceptions import EntityNotFoundError, DomainException
from app.infrastructure.config import RepositoryContainer
from app.application.use_cases import (
    GetProductUseCase,
    SearchProductsUseCase,
    ListProductsByCategoryUseCase,
    ListProductsBySellerUseCase,
    CreateProductUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase
)
from app.application.dtos import CreateProductRequest, UpdateProductRequest
from app.presentation.schemas import (
    ProductSchema,
    CreateProductSchema,
    UpdateProductSchema
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: UUID,
    repo: ProductRepository = Depends(RepositoryContainer.get_product_repository)
):
    """Get a product by ID."""
    try:
        use_case = GetProductUseCase(repo)
        dto = await use_case.execute(product_id)
        return {
            "id": dto.id,
            "name": dto.name,
            "description": dto.description,
            "sku": dto.sku,
            "price": dto.price,
            "currency": dto.currency,
            "category_id": dto.category_id,
            "seller_id": dto.seller_id,
            "stock_quantity": dto.stock_quantity,
            "is_active": dto.is_active,
            "created_at": dto.created_at,
            "updated_at": dto.updated_at
        }
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/search/query", response_model=List[ProductSchema])
async def search_products(
    q: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 50,
    repo: ProductRepository = Depends(RepositoryContainer.get_product_repository)
):
    """Search products."""
    try:
        use_case = SearchProductsUseCase(repo)
        dtos = await use_case.execute(q, skip, limit)
        return [
            {
                "id": dto.id,
                "name": dto.name,
                "description": dto.description,
                "sku": dto.sku,
                "price": dto.price,
                "currency": dto.currency,
                "category_id": dto.category_id,
                "seller_id": dto.seller_id,
                "stock_quantity": dto.stock_quantity,
                "is_active": dto.is_active,
                "created_at": dto.created_at,
                "updated_at": dto.updated_at
            }
            for dto in dtos
        ]
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/category/{category_id}", response_model=List[ProductSchema])
async def get_products_by_category(
    category_id: UUID,
    skip: int = 0,
    limit: int = 50,
    repo: ProductRepository = Depends(RepositoryContainer.get_product_repository)
):
    """Get products by category."""
    try:
        use_case = ListProductsByCategoryUseCase(repo)
        dtos = await use_case.execute(category_id, skip, limit)
        return [
            {
                "id": dto.id,
                "name": dto.name,
                "description": dto.description,
                "sku": dto.sku,
                "price": dto.price,
                "currency": dto.currency,
                "category_id": dto.category_id,
                "seller_id": dto.seller_id,
                "stock_quantity": dto.stock_quantity,
                "is_active": dto.is_active,
                "created_at": dto.created_at,
                "updated_at": dto.updated_at
            }
            for dto in dtos
        ]
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/seller/{seller_id}", response_model=List[ProductSchema])
async def get_products_by_seller(
    seller_id: UUID,
    skip: int = 0,
    limit: int = 50,
    repo: ProductRepository = Depends(RepositoryContainer.get_product_repository)
):
    """Get products by seller."""
    try:
        use_case = ListProductsBySellerUseCase(repo)
        dtos = await use_case.execute(seller_id, skip, limit)
        return [
            {
                "id": dto.id,
                "name": dto.name,
                "description": dto.description,
                "sku": dto.sku,
                "price": dto.price,
                "currency": dto.currency,
                "category_id": dto.category_id,
                "seller_id": dto.seller_id,
                "stock_quantity": dto.stock_quantity,
                "is_active": dto.is_active,
                "created_at": dto.created_at,
                "updated_at": dto.updated_at
            }
            for dto in dtos
        ]
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    schema: CreateProductSchema,
    seller_id: UUID,  # Should come from auth
    cat_repo: CategoryRepository = Depends(RepositoryContainer.get_category_repository),
    prod_repo: ProductRepository = Depends(RepositoryContainer.get_product_repository)
):
    """Create a new product."""
    try:
        request = CreateProductRequest(
            name=schema.name,
            description=schema.description,
            sku=schema.sku,
            price=schema.price,
            category_id=schema.category_id,
            stock_quantity=schema.stock_quantity
        )
        use_case = CreateProductUseCase(prod_repo, cat_repo)
        dto = await use_case.execute(request, seller_id)
        return {
            "id": dto.id,
            "name": dto.name,
            "description": dto.description,
            "sku": dto.sku,
            "price": dto.price,
            "currency": dto.currency,
            "category_id": dto.category_id,
            "seller_id": dto.seller_id,
            "stock_quantity": dto.stock_quantity,
            "is_active": dto.is_active,
            "created_at": dto.created_at,
            "updated_at": dto.updated_at
        }
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: UUID,
    schema: UpdateProductSchema,
    seller_id: UUID,  # Should come from auth
    repo: ProductRepository = Depends(RepositoryContainer.get_product_repository)
):
    """Update a product."""
    try:
        request = UpdateProductRequest(
            name=schema.name,
            description=schema.description,
            price=schema.price,
            stock_quantity=schema.stock_quantity,
            is_active=schema.is_active
        )
        use_case = UpdateProductUseCase(repo)
        dto = await use_case.execute(product_id, request, seller_id)
        return {
            "id": dto.id,
            "name": dto.name,
            "description": dto.description,
            "sku": dto.sku,
            "price": dto.price,
            "currency": dto.currency,
            "category_id": dto.category_id,
            "seller_id": dto.seller_id,
            "stock_quantity": dto.stock_quantity,
            "is_active": dto.is_active,
            "created_at": dto.created_at,
            "updated_at": dto.updated_at
        }
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    seller_id: UUID,  # Should come from auth
    repo: ProductRepository = Depends(RepositoryContainer.get_product_repository)
):
    """Delete a product."""
    try:
        use_case = DeleteProductUseCase(repo)
        await use_case.execute(product_id, seller_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
