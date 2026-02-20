# backend/app/models/order_item.py
import uuid
from sqlalchemy import Column, ForeignKey, DECIMAL, Integer, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("sellers.id"))
    product_name = Column(String(150), nullable=False)
    unit_price = Column(DECIMAL(10,2), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(DECIMAL(10,2), nullable=False)
    marketplace_commission = Column(DECIMAL(10,2), nullable=False)
    seller_income = Column(DECIMAL(10,2), nullable=False)
