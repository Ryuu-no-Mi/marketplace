"""Domain entities."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from decimal import Decimal

from app.domain.value_objects import Money, Email, Address, PhoneNumber, ProductDimensions
from app.domain.exceptions import InvalidEntityError, InsufficientInventoryError


@dataclass
class BaseEntity:
    """Base class for all domain entities."""
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Category(BaseEntity):
    """Category entity."""
    name: str
    description: str
    is_active: bool = True

    def __post_init__(self):
        if not self.name or len(self.name) < 2:
            raise InvalidEntityError("Category name must be at least 2 characters")


@dataclass
class Product(BaseEntity):
    """Product entity."""
    name: str
    description: str
    sku: str
    price: Money
    category_id: UUID
    seller_id: UUID
    stock_quantity: int
    dimensions: Optional[ProductDimensions] = None
    is_active: bool = True

    def __post_init__(self):
        if not self.name or len(self.name) < 3:
            raise InvalidEntityError("Product name must be at least 3 characters")
        if self.stock_quantity < 0:
            raise InvalidEntityError("Stock quantity cannot be negative")
        if not self.sku or len(self.sku) < 3:
            raise InvalidEntityError("SKU must be at least 3 characters")

    def reduce_stock(self, quantity: int) -> None:
        """Reduce product stock."""
        if quantity <= 0:
            raise InvalidEntityError("Quantity must be positive")
        if self.stock_quantity < quantity:
            raise InsufficientInventoryError(f"Insufficient inventory. Available: {self.stock_quantity}")
        self.stock_quantity -= quantity
        self.updated_at = datetime.utcnow()

    def increase_stock(self, quantity: int) -> None:
        """Increase product stock."""
        if quantity <= 0:
            raise InvalidEntityError("Quantity must be positive")
        self.stock_quantity += quantity
        self.updated_at = datetime.utcnow()


@dataclass
class User(BaseEntity):
    """User entity."""
    email: Email
    first_name: str
    last_name: str
    phone_number: Optional[PhoneNumber] = None
    address: Optional[Address] = None
    is_active: bool = True

    def __post_init__(self):
        if not self.first_name or len(self.first_name) < 2:
            raise InvalidEntityError("First name must be at least 2 characters")
        if not self.last_name or len(self.last_name) < 2:
            raise InvalidEntityError("Last name must be at least 2 characters")


@dataclass
class Seller(BaseEntity):
    """Seller entity."""
    user_id: UUID
    business_name: str
    tax_id: str
    is_verified: bool = False
    total_sales: Money = field(default_factory=lambda: Money(Decimal("0.00")))
    rating: float = field(default=0.0)

    def __post_init__(self):
        if not self.business_name or len(self.business_name) < 3:
            raise InvalidEntityError("Business name must be at least 3 characters")
        if not self.tax_id or len(self.tax_id) < 5:
            raise InvalidEntityError("Tax ID must be at least 5 characters")
        if rating < 0 or self.rating > 5:
            raise InvalidEntityError("Rating must be between 0 and 5")


@dataclass
class OrderItem(BaseEntity):
    """Order item entity."""
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Money
    subtotal: Money

    def __post_init__(self):
        if self.quantity <= 0:
            raise InvalidEntityError("Quantity must be positive")
        expected_subtotal = Money(self.unit_price.amount * self.quantity, self.unit_price.currency)
        if self.subtotal != expected_subtotal:
            raise InvalidEntityError("Subtotal doesn't match unit price × quantity")


@dataclass
class Order(BaseEntity):
    """Order entity."""
    user_id: UUID
    status: str  # pending, processing, shipped, delivered, cancelled
    shipping_address: Address
    total_amount: Money
    items: List[OrderItem] = field(default_factory=list)

    def __post_init__(self):
        valid_statuses = {"pending", "processing", "shipped", "delivered", "cancelled"}
        if self.status not in valid_statuses:
            raise InvalidEntityError(f"Invalid status. Must be one of {valid_statuses}")
        if not self.items:
            raise InvalidEntityError("Order must have at least one item")

    def calculate_total(self) -> Money:
        """Calculate total order amount."""
        total = Money(Decimal("0.00"), self.total_amount.currency)
        for item in self.items:
            total = total + item.subtotal
        return total


@dataclass
class Payment(BaseEntity):
    """Payment entity."""
    order_id: UUID
    seller_id: UUID
    amount: Money
    status: str  # pending, completed, failed, refunded
    payment_method: str  # credit_card, debit_card, paypal, etc.
    transaction_id: Optional[str] = None

    def __post_init__(self):
        valid_statuses = {"pending", "completed", "failed", "refunded"}
        if self.status not in valid_statuses:
            raise InvalidEntityError(f"Invalid status. Must be one of {valid_statuses}")
