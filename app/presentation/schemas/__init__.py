"""API Schemas for request/response validation."""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class CategorySchema(BaseModel):
    """Category response schema."""
    id: UUID
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateCategorySchema(BaseModel):
    """Create category request schema."""
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5, max_length=500)


class UpdateCategorySchema(BaseModel):
    """Update category request schema."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=500)
    is_active: Optional[bool] = None


class ProductSchema(BaseModel):
    """Product response schema."""
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

    class Config:
        from_attributes = True


class CreateProductSchema(BaseModel):
    """Create product request schema."""
    name: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=2000)
    sku: str = Field(..., min_length=3, max_length=50)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category_id: UUID
    stock_quantity: int = Field(..., ge=0)


class UpdateProductSchema(BaseModel):
    """Update product request schema."""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class UserSchema(BaseModel):
    """User response schema."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateUserSchema(BaseModel):
    """Create user request schema."""
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone_number: Optional[str] = None


class UpdateUserSchema(BaseModel):
    """Update user request schema."""
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = None


class SellerSchema(BaseModel):
    """Seller response schema."""
    id: UUID
    user_id: UUID
    business_name: str
    tax_id: str
    is_verified: bool
    total_sales: Decimal
    rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateSellerSchema(BaseModel):
    """Create seller request schema."""
    user_id: UUID
    business_name: str = Field(..., min_length=3, max_length=200)
    tax_id: str = Field(..., min_length=5, max_length=50)


class OrderItemSchema(BaseModel):
    """Order item schema."""
    id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class OrderSchema(BaseModel):
    """Order response schema."""
    id: UUID
    user_id: UUID
    status: str
    total_amount: Decimal
    items: List[OrderItemSchema]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateOrderItemSchema(BaseModel):
    """Create order item request schema."""
    product_id: UUID
    quantity: int = Field(..., gt=0)


class CreateOrderSchema(BaseModel):
    """Create order request schema."""
    items: List[CreateOrderItemSchema]
    shipping_address_street: str
    shipping_address_city: str
    shipping_address_state: str
    shipping_address_postal_code: str
    shipping_address_country: str


class PaymentSchema(BaseModel):
    """Payment response schema."""
    id: UUID
    order_id: UUID
    seller_id: UUID
    amount: Decimal
    status: str
    payment_method: str
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreatePaymentSchema(BaseModel):
    """Create payment request schema."""
    order_id: UUID
    seller_id: UUID
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    payment_method: str
