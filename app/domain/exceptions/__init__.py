"""Domain exceptions module."""


class DomainException(Exception):
    """Base exception for domain errors."""
    pass


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""
    pass


class InvalidEntityError(DomainException):
    """Raised when an entity has invalid state."""
    pass


class DuplicateEntityError(DomainException):
    """Raised when trying to create a duplicate entity."""
    pass


class InsufficientInventoryError(DomainException):
    """Raised when there's insufficient inventory."""
    pass


class InvalidOrderError(DomainException):
    """Raised when an order is invalid."""
    pass


class PaymentFailedError(DomainException):
    """Raised when a payment operation fails."""
    pass
