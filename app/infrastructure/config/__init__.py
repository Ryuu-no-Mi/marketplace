"""Dependency injection configuration."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.infrastructure.repositories import (
    SQLAlchemyCategoryRepository,
    SQLAlchemyProductRepository,
    SQLAlchemyUserRepository,
    SQLAlchemySellerRepository,
    SQLAlchemyOrderRepository,
    SQLAlchemyPaymentRepository
)
from app.domain.ports import (
    CategoryRepository,
    ProductRepository,
    UserRepository,
    SellerRepository,
    OrderRepository,
    PaymentRepository
)


class RepositoryContainer:
    """Container for repository dependencies."""

    @staticmethod
    async def get_category_repository(
        session: AsyncSession = Depends(get_db_session)
    ) -> CategoryRepository:
        """Get category repository instance."""
        return SQLAlchemyCategoryRepository(session)

    @staticmethod
    async def get_product_repository(
        session: AsyncSession = Depends(get_db_session)
    ) -> ProductRepository:
        """Get product repository instance."""
        return SQLAlchemyProductRepository(session)

    @staticmethod
    async def get_user_repository(
        session: AsyncSession = Depends(get_db_session)
    ) -> UserRepository:
        """Get user repository instance."""
        return SQLAlchemyUserRepository(session)

    @staticmethod
    async def get_seller_repository(
        session: AsyncSession = Depends(get_db_session)
    ) -> SellerRepository:
        """Get seller repository instance."""
        return SQLAlchemySellerRepository(session)

    @staticmethod
    async def get_order_repository(
        session: AsyncSession = Depends(get_db_session)
    ) -> OrderRepository:
        """Get order repository instance."""
        return SQLAlchemyOrderRepository(session)

    @staticmethod
    async def get_payment_repository(
        session: AsyncSession = Depends(get_db_session)
    ) -> PaymentRepository:
        """Get payment repository instance."""
        return SQLAlchemyPaymentRepository(session)
