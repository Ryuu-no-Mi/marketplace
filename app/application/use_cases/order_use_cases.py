"""Order use cases."""

from uuid import UUID
from typing import List
from decimal import Decimal

from app.domain.entities import Order, OrderItem
from app.domain.value_objects import Money, Address
from app.domain.ports import (
    OrderRepository, ProductRepository, UserRepository
)
from app.domain.exceptions import EntityNotFoundError, InvalidEntityError
from app.application.dtos import (
    OrderDTO, CreateOrderRequest
)
from app.application.mappers import OrderMapper


class GetOrderUseCase:
    """Use case for getting an order by ID."""

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def execute(self, order_id: UUID) -> OrderDTO:
        """Get order by ID."""
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise EntityNotFoundError(f"Order {order_id} not found")
        return OrderMapper.to_dto(order)


class ListUserOrdersUseCase:
    """Use case for listing user's orders."""

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def execute(self, user_id: UUID, skip: int = 0, limit: int = 50) -> List[OrderDTO]:
        """Get user's orders."""
        orders = await self.repository.get_by_user_id(user_id, skip, limit)
        return [OrderMapper.to_dto(o) for o in orders]


class CreateOrderUseCase:
    """Use case for creating an order."""

    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        user_repository: UserRepository
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.user_repository = user_repository

    async def execute(self, user_id: UUID, request: CreateOrderRequest) -> OrderDTO:
        """Create a new order."""
        # Verify user exists
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError(f"User {user_id} not found")

        # Build shipping address
        shipping_address = Address(
            street=request.shipping_address_street,
            city=request.shipping_address_city,
            state=request.shipping_address_state,
            postal_code=request.shipping_address_postal_code,
            country=request.shipping_address_country
        )

        # Build order items and calculate total
        order_items = []
        total = Money(Decimal("0.00"))

        for item_request in request.items:
            product = await self.product_repository.get_by_id(item_request.product_id)
            if not product:
                raise EntityNotFoundError(f"Product {item_request.product_id} not found")

            # Reduce stock
            product.reduce_stock(item_request.quantity)
            await self.product_repository.update(product)

            # Create order item
            subtotal = Money(
                product.price.amount * item_request.quantity,
                product.price.currency
            )
            order_item = OrderItem(
                order_id=UUID('00000000-0000-0000-0000-000000000000'),  # Temporary
                product_id=product.id,
                quantity=item_request.quantity,
                unit_price=product.price,
                subtotal=subtotal
            )
            order_items.append(order_item)
            total = total + subtotal

        # Create order
        order = Order(
            user_id=user_id,
            status="pending",
            shipping_address=shipping_address,
            total_amount=total,
            items=order_items
        )

        # Update order item references
        for item in order.items:
            object.__setattr__(item, 'order_id', order.id)

        saved = await self.order_repository.add(order)
        return OrderMapper.to_dto(saved)


class UpdateOrderStatusUseCase:
    """Use case for updating order status."""

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def execute(self, order_id: UUID, new_status: str) -> OrderDTO:
        """Update order status."""
        valid_statuses = {"pending", "processing", "shipped", "delivered", "cancelled"}
        if new_status not in valid_statuses:
            raise InvalidEntityError(f"Invalid status. Must be one of {valid_statuses}")

        order = await self.repository.get_by_id(order_id)
        if not order:
            raise EntityNotFoundError(f"Order {order_id} not found")

        order.status = new_status
        updated = await self.repository.update(order)
        return OrderMapper.to_dto(updated)


class CancelOrderUseCase:
    """Use case for canceling an order."""

    def __init__(self, repository: OrderRepository, product_repository: ProductRepository):
        self.repository = repository
        self.product_repository = product_repository

    async def execute(self, order_id: UUID) -> OrderDTO:
        """Cancel an order and restore inventory."""
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise EntityNotFoundError(f"Order {order_id} not found")

        # Restore product inventory
        for item in order.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if product:
                product.increase_stock(item.quantity)
                await self.product_repository.update(product)

        order.status = "cancelled"
        updated = await self.repository.update(order)
        return OrderMapper.to_dto(updated)
