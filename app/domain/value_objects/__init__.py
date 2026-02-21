"""Value Objects for domain models."""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    """Value object representing monetary amount."""
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Currency must be a valid 3-letter code")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)


@dataclass(frozen=True)
class Email:
    """Value object representing email."""
    value: str

    def __post_init__(self):
        if "@" not in self.value or "." not in self.value.split("@")[1]:
            raise ValueError("Invalid email format")


@dataclass(frozen=True)
class PhoneNumber:
    """Value object representing phone number."""
    value: str
    country_code: str = "+1"

    def __post_init__(self):
        if not self.value.replace("-", "").replace(" ", "").isdigit():
            raise ValueError("Phone number must contain only digits, spaces, or hyphens")


@dataclass(frozen=True)
class Address:
    """Value object representing physical address."""
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    apartment: Optional[str] = None

    def __post_init__(self):
        if not all([self.street, self.city, self.state, self.postal_code, self.country]):
            raise ValueError("All address fields are required")


@dataclass(frozen=True)
class ProductDimensions:
    """Value object representing product dimensions."""
    length: float
    width: float
    height: float
    weight: float

    def __post_init__(self):
        if any(x <= 0 for x in [self.length, self.width, self.height, self.weight]):
            raise ValueError("All dimensions must be positive")
