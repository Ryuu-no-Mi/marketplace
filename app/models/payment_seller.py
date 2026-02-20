# backend/app/models/payment_seller.py
import uuid
from sqlalchemy import Column, ForeignKey, DECIMAL, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class PaymentSeller(Base):
    __tablename__ = "payments_sellers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    seller_id = Column(UUID(as_uuid=True), ForeignKey("sellers.id"))
    gross_amount = Column(DECIMAL(10,2))
    commission = Column(DECIMAL(10,2))
    net_amount = Column(DECIMAL(10,2))
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
