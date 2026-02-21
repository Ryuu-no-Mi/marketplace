"""Product use cases."""

from uuid import UUID
from typing import List, Optional

from app.domain.entities import Product
from app.domain.value_objects import Money
from app.domain.ports import ProductRepository, CategoryRepository
from app.domain.exceptions import EntityNotFoundError, InvalidEntityError
from app.application.dtos import (
    ProductDTO, CreateProductRequest, UpdateProductRequest
)
from app.application.mappers import ProductMapper


class GetProductUseCase:
    """Use case for getting a product by ID."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, product_id: UUID) -> ProductDTO:
        """Get product by ID."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise EntityNotFoundError(f"Product {product_id} not found")
        return ProductMapper.to_dto(product)


class SearchProductsUseCase:
    """Use case for searching products."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, query: str, skip: int = 0, limit: int = 50) -> List[ProductDTO]:
        """Search products by query."""
        products = await self.repository.search(query, skip, limit)
        return [ProductMapper.to_dto(p) for p in products]


class ListProductsByCategoryUseCase:
    """Use case for listing products by category."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, category_id: UUID, skip: int = 0, limit: int = 50) -> List[ProductDTO]:
        """Get products by category."""
        products = await self.repository.get_by_category_id(category_id, skip, limit)
        return [ProductMapper.to_dto(p) for p in products]


class ListProductsBySellerUseCase:
    """Use case for listing products by seller."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, seller_id: UUID, skip: int = 0, limit: int = 50) -> List[ProductDTO]:
        """Get products by seller."""
        products = await self.repository.get_by_seller_id(seller_id, skip, limit)
        return [ProductMapper.to_dto(p) for p in products]


class CreateProductUseCase:
    """Use case for creating a product."""

    def __init__(self, repository: ProductRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    async def execute(self, request: CreateProductRequest, seller_id: UUID) -> ProductDTO:
        """Create a new product."""
        # Verify category exists
        category = await self.category_repository.get_by_id(request.category_id)
        if not category:
            raise EntityNotFoundError(f"Category {request.category_id} not found")

        # Create product entity
        product = Product(
            name=request.name,
            description=request.description,
            sku=request.sku,
            price=Money(request.price),
            category_id=request.category_id,
            seller_id=seller_id,
            stock_quantity=request.stock_quantity
        )

        saved = await self.repository.add(product)
        return ProductMapper.to_dto(saved)


class UpdateProductUseCase:
    """Use case for updating a product."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, product_id: UUID, request: UpdateProductRequest, seller_id: UUID) -> ProductDTO:
        """Update a product."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise EntityNotFoundError(f"Product {product_id} not found")

        # Verify seller owns the product
        if product.seller_id != seller_id:
            raise InvalidEntityError("Seller does not own this product")

        # Update fields
        if request.name:
            product.name = request.name
        if request.description:
            product.description = request.description
        if request.price:
            product.price = Money(request.price, product.price.currency)
        if request.stock_quantity is not None:
            product.stock_quantity = request.stock_quantity
        if request.is_active is not None:
            product.is_active = request.is_active

        updated = await self.repository.update(product)
        return ProductMapper.to_dto(updated)


class DeleteProductUseCase:
    """Use case for deleting a product."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, product_id: UUID, seller_id: UUID) -> bool:
        """Delete a product."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise EntityNotFoundError(f"Product {product_id} not found")

        # Verify seller owns the product
        if product.seller_id != seller_id:
            raise InvalidEntityError("Seller does not own this product")

        return await self.repository.delete(product_id)
