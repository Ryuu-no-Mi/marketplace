"""Repository implementations using SQLAlchemy."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities import Category, Product, User, Seller, Order, Payment
from app.domain.ports import (
    CategoryRepository, ProductRepository, UserRepository,
    SellerRepository, OrderRepository, PaymentRepository
)


class SQLAlchemyCategoryRepository(CategoryRepository):
    """Category repository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, category: Category) -> Category:
        """Add a new category."""
        # Implementation will depend on ORM model
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        """Get category by ID."""
        stmt = select(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[Category]:
        """Get all categories."""
        stmt = select(Category).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, category: Category) -> Category:
        """Update a category."""
        await self.session.merge(category)
        await self.session.commit()
        return category

    async def delete(self, category_id: UUID) -> bool:
        """Delete a category."""
        category = await self.get_by_id(category_id)
        if not category:
            return False
        await self.session.delete(category)
        await self.session.commit()
        return True


class SQLAlchemyProductRepository(ProductRepository):
    """Product repository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, product: Product) -> Product:
        """Add a new product."""
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Get product by ID."""
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_seller_id(self, seller_id: UUID, skip: int = 0, limit: int = 50) -> List[Product]:
        """Get products by seller ID."""
        stmt = select(Product).where(Product.seller_id == seller_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_category_id(self, category_id: UUID, skip: int = 0, limit: int = 50) -> List[Product]:
        """Get products by category ID."""
        stmt = select(Product).where(Product.category_id == category_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search(self, query: str, skip: int = 0, limit: int = 50) -> List[Product]:
        """Search products by name or description."""
        stmt = select(Product).where(
            (Product.name.ilike(f"%{query}%")) | (Product.description.ilike(f"%{query}%"))
        ).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, product: Product) -> Product:
        """Update a product."""
        await self.session.merge(product)
        await self.session.commit()
        return product

    async def delete(self, product_id: UUID) -> bool:
        """Delete a product."""
        product = await self.get_by_id(product_id)
        if not product:
            return False
        await self.session.delete(product)
        await self.session.commit()
        return True


class SQLAlchemyUserRepository(UserRepository):
    """User repository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> User:
        """Add a new user."""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        # Implementation depends on how Email VO is stored
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        """Update a user."""
        await self.session.merge(user)
        await self.session.commit()
        return user

    async def delete(self, user_id: UUID) -> bool:
        """Delete a user."""
        user = await self.get_by_id(user_id)
        if not user:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True


class SQLAlchemySellerRepository(SellerRepository):
    """Seller repository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, seller: Seller) -> Seller:
        """Add a new seller."""
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller

    async def get_by_id(self, seller_id: UUID) -> Optional[Seller]:
        """Get seller by ID."""
        stmt = select(Seller).where(Seller.id == seller_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> Optional[Seller]:
        """Get seller by user ID."""
        stmt = select(Seller).where(Seller.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 50) -> List[Seller]:
        """Get all sellers."""
        stmt = select(Seller).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, seller: Seller) -> Seller:
        """Update a seller."""
        await self.session.merge(seller)
        await self.session.commit()
        return seller

    async def delete(self, seller_id: UUID) -> bool:
        """Delete a seller."""
        seller = await self.get_by_id(seller_id)
        if not seller:
            return False
        await self.session.delete(seller)
        await self.session.commit()
        return True


class SQLAlchemyOrderRepository(OrderRepository):
    """Order repository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, order: Order) -> Order:
        """Add a new order."""
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Get order by ID."""
        stmt = select(Order).where(Order.id == order_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 50) -> List[Order]:
        """Get orders by user ID."""
        stmt = select(Order).where(Order.user_id == user_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, order: Order) -> Order:
        """Update an order."""
        await self.session.merge(order)
        await self.session.commit()
        return order

    async def delete(self, order_id: UUID) -> bool:
        """Delete an order."""
        order = await self.get_by_id(order_id)
        if not order:
            return False
        await self.session.delete(order)
        await self.session.commit()
        return True


class SQLAlchemyPaymentRepository(PaymentRepository):
    """Payment repository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, payment: Payment) -> Payment:
        """Add a new payment."""
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_by_id(self, payment_id: UUID) -> Optional[Payment]:
        """Get payment by ID."""
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_order_id(self, order_id: UUID) -> Optional[Payment]:
        """Get payment by order ID."""
        stmt = select(Payment).where(Payment.order_id == order_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_seller_id(self, seller_id: UUID, skip: int = 0, limit: int = 50) -> List[Payment]:
        """Get payments by seller ID."""
        stmt = select(Payment).where(Payment.seller_id == seller_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, payment: Payment) -> Payment:
        """Update a payment."""
        await self.session.merge(payment)
        await self.session.commit()
        return payment
