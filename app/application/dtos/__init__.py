"""Data Transfer Objects for application layer."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from decimal import Decimal


@dataclass
class CategoryDTO:
    """Category data transfer object."""
    id: UUID
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class CreateCategoryRequest:
    """Request to create a category."""
    name: str
    description: str


@dataclass
class UpdateCategoryRequest:
    """Request to update a category."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class ProductDTO:
    """Product data transfer object."""
    id: UUID
    name: str
    description: str
    sku: str
    price: Decimal
    currency: str
    category_id: UUID
    seller_id: UUID
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class CreateProductRequest:
    """Request to create a product."""
    name: str
    description: str
    sku: str
    price: Decimal
    category_id: UUID
    stock_quantity: int


@dataclass
class UpdateProductRequest:
    """Request to update a product."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None


@dataclass
class UserDTO:
    """User data transfer object."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateUserRequest:
    """Request to create a user."""
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None


@dataclass
class UpdateUserRequest:
    """Request to update a user."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


@dataclass
class SellerDTO:
    """Seller data transfer object."""
    id: UUID
    user_id: UUID
    business_name: str
    tax_id: str
    is_verified: bool
    total_sales: Decimal
    rating: float
    created_at: datetime
    updated_at: datetime


@dataclass
class CreateSellerRequest:
    """Request to create a seller."""
    user_id: UUID
    business_name: str
    tax_id: str


@dataclass
class OrderItemDTO:
    """Order item data transfer object."""
    id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


@dataclass
class CreateOrderItemRequest:
    """Request to create an order item."""
    product_id: UUID
    quantity: int


@dataclass
class OrderDTO:
    """Order data transfer object."""
    id: UUID
    user_id: UUID
    status: str
    total_amount: Decimal
    items: List[OrderItemDTO]
    created_at: datetime
    updated_at: datetime


@dataclass
class CreateOrderRequest:
    """Request to create an order."""
    items: List[CreateOrderItemRequest]
    shipping_address_street: str
    shipping_address_city: str
    shipping_address_state: str
    shipping_address_postal_code: str
    shipping_address_country: str


@dataclass
class PaymentDTO:
    """Payment data transfer object."""
    id: UUID
    order_id: UUID
    seller_id: UUID
    amount: Decimal
    status: str
    payment_method: str
    transaction_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreatePaymentRequest:
    """Request to create a payment."""
    order_id: UUID
    seller_id: UUID
    amount: Decimal
    payment_method: str
