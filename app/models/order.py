# backend/app/models/order.py
import uuid
from sqlalchemy import Column, ForeignKey, DECIMAL, Enum, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    guest_email = Column(String(150), nullable=True)
    total_amount = Column(DECIMAL(10,2), nullable=False)
    status = Column(Enum('pending','paid','shipped','completed','cancelled', name="order_status"), default='pending')
    tracking_number = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

