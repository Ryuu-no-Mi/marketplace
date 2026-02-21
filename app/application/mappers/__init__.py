"""Mappers for converting between entities and DTOs."""

from decimal import Decimal
from app.domain.entities import (
    Category, Product, User, Seller, Order, OrderItem, Payment
)
from app.domain.value_objects import Money, Email, PhoneNumber, Address
from app.application.dtos import (
    CategoryDTO, ProductDTO, UserDTO, SellerDTO, OrderDTO, OrderItemDTO, PaymentDTO
)


class CategoryMapper:
    """Mapper for Category entity."""

    @staticmethod
    def to_dto(entity: Category) -> CategoryDTO:
        """Convert category entity to DTO."""
        return CategoryDTO(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity(dto: CategoryDTO) -> Category:
        """Convert category DTO to entity."""
        return Category(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )


class ProductMapper:
    """Mapper for Product entity."""

    @staticmethod
    def to_dto(entity: Product) -> ProductDTO:
        """Convert product entity to DTO."""
        return ProductDTO(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            sku=entity.sku,
            price=entity.price.amount,
            currency=entity.price.currency,
            category_id=entity.category_id,
            seller_id=entity.seller_id,
            stock_quantity=entity.stock_quantity,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity(dto: ProductDTO) -> Product:
        """Convert product DTO to entity."""
        return Product(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            sku=dto.sku,
            price=Money(dto.price, dto.currency),
            category_id=dto.category_id,
            seller_id=dto.seller_id,
            stock_quantity=dto.stock_quantity,
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )


class UserMapper:
    """Mapper for User entity."""

    @staticmethod
    def to_dto(entity: User) -> UserDTO:
        """Convert user entity to DTO."""
        return UserDTO(
            id=entity.id,
            email=entity.email.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            phone_number=entity.phone_number.value if entity.phone_number else None,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity(dto: UserDTO) -> User:
        """Convert user DTO to entity."""
        return User(
            id=dto.id,
            email=Email(dto.email),
            first_name=dto.first_name,
            last_name=dto.last_name,
            phone_number=PhoneNumber(dto.phone_number) if dto.phone_number else None,
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )


class SellerMapper:
    """Mapper for Seller entity."""

    @staticmethod
    def to_dto(entity: Seller) -> SellerDTO:
        """Convert seller entity to DTO."""
        return SellerDTO(
            id=entity.id,
            user_id=entity.user_id,
            business_name=entity.business_name,
            tax_id=entity.tax_id,
            is_verified=entity.is_verified,
            total_sales=entity.total_sales.amount,
            rating=entity.rating,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity(dto: SellerDTO) -> Seller:
        """Convert seller DTO to entity."""
        return Seller(
            id=dto.id,
            user_id=dto.user_id,
            business_name=dto.business_name,
            tax_id=dto.tax_id,
            is_verified=dto.is_verified,
            total_sales=Money(dto.total_sales),
            rating=dto.rating,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )


class OrderItemMapper:
    """Mapper for OrderItem entity."""

    @staticmethod
    def to_dto(entity: OrderItem) -> OrderItemDTO:
        """Convert order item entity to DTO."""
        return OrderItemDTO(
            id=entity.id,
            product_id=entity.product_id,
            quantity=entity.quantity,
            unit_price=entity.unit_price.amount,
            subtotal=entity.subtotal.amount
        )


class OrderMapper:
    """Mapper for Order entity."""

    @staticmethod
    def to_dto(entity: Order) -> OrderDTO:
        """Convert order entity to DTO."""
        return OrderDTO(
            id=entity.id,
            user_id=entity.user_id,
            status=entity.status,
            total_amount=entity.total_amount.amount,
            items=[OrderItemMapper.to_dto(item) for item in entity.items],
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )


class PaymentMapper:
    """Mapper for Payment entity."""

    @staticmethod
    def to_dto(entity: Payment) -> PaymentDTO:
        """Convert payment entity to DTO."""
        return PaymentDTO(
            id=entity.id,
            order_id=entity.order_id,
            seller_id=entity.seller_id,
            amount=entity.amount.amount,
            status=entity.status,
            payment_method=entity.payment_method,
            transaction_id=entity.transaction_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity(dto: PaymentDTO) -> Payment:
        """Convert payment DTO to entity."""
        return Payment(
            id=dto.id,
            order_id=dto.order_id,
            seller_id=dto.seller_id,
            amount=Money(dto.amount),
            status=dto.status,
            payment_method=dto.payment_method,
            transaction_id=dto.transaction_id
        )
