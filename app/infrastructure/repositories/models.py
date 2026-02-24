"""
Modelos SQLAlchemy para la base de datos.
Estos son detalles técnicos de infraestructura.
Las entidades de dominio no deben conocer de estos modelos.

Aquí van todos los detalles SQL: tipos, restricciones, índices, relaciones, etc.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from datetime import datetime


class UserModel(Base):
    """
    Modelo SQLAlchemy para la tabla de usuarios.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    role = Column(SQLEnum('admin', 'seller', 'customer', name='user_roles'), default='customer')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class ProductModel(Base):
    """
    Modelo SQLAlchemy para la tabla de productos.
    Este es un detalle de infraestructura, separado de la entidad de dominio.
    El dominio no debe conocer de SQLAlchemy.
    """
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
