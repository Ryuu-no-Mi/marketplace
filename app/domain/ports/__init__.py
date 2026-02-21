"""Repository ports (interfaces) for domain layer."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities import (
    Category, Product, User, Seller, Order, Payment
)


class CategoryRepository(ABC):
    """Port for category persistence."""

    @abstractmethod
    async def add(self, category: Category) -> Category:
        """Add a new category."""
        pass

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        """Get category by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 10) -> List[Category]:
        """Get all categories."""
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        """Update a category."""
        pass

    @abstractmethod
    async def delete(self, category_id: UUID) -> bool:
        """Delete a category."""
        pass


class ProductRepository(ABC):
    """Port for product persistence."""

    @abstractmethod
    async def add(self, product: Product) -> Product:
        """Add a new product."""
        pass

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Get product by ID."""
        pass

    @abstractmethod
    async def get_by_seller_id(self, seller_id: UUID, skip: int = 0, limit: int = 50) -> List[Product]:
        """Get products by seller ID."""
        pass

    @abstractmethod
    async def get_by_category_id(self, category_id: UUID, skip: int = 0, limit: int = 50) -> List[Product]:
        """Get products by category ID."""
        pass

    @abstractmethod
    async def search(self, query: str, skip: int = 0, limit: int = 50) -> List[Product]:
        """Search products by name or description."""
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        """Update a product."""
        pass

    @abstractmethod
    async def delete(self, product_id: UUID) -> bool:
        """Delete a product."""
        pass


class UserRepository(ABC):
    """Port for user persistence."""

    @abstractmethod
    async def add(self, user: User) -> User:
        """Add a new user."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update a user."""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete a user."""
        pass


class SellerRepository(ABC):
    """Port for seller persistence."""

    @abstractmethod
    async def add(self, seller: Seller) -> Seller:
        """Add a new seller."""
        pass

    @abstractmethod
    async def get_by_id(self, seller_id: UUID) -> Optional[Seller]:
        """Get seller by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[Seller]:
        """Get seller by user ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 50) -> List[Seller]:
        """Get all sellers."""
        pass

    @abstractmethod
    async def update(self, seller: Seller) -> Seller:
        """Update a seller."""
        pass

    @abstractmethod
    async def delete(self, seller_id: UUID) -> bool:
        """Delete a seller."""
        pass


class OrderRepository(ABC):
    """Port for order persistence."""

    @abstractmethod
    async def add(self, order: Order) -> Order:
        """Add a new order."""
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Get order by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 50) -> List[Order]:
        """Get orders by user ID."""
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        """Update an order."""
        pass

    @abstractmethod
    async def delete(self, order_id: UUID) -> bool:
        """Delete an order."""
        pass


class PaymentRepository(ABC):
    """Port for payment persistence."""

    @abstractmethod
    async def add(self, payment: Payment) -> Payment:
        """Add a new payment."""
        pass

    @abstractmethod
    async def get_by_id(self, payment_id: UUID) -> Optional[Payment]:
        """Get payment by ID."""
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> Optional[Payment]:
        """Get payment by order ID."""
        pass

    @abstractmethod
    async def get_by_seller_id(self, seller_id: UUID, skip: int = 0, limit: int = 50) -> List[Payment]:
        """Get payments by seller ID."""
        pass

    @abstractmethod
    async def update(self, payment: Payment) -> Payment:
        """Update a payment."""
        pass
