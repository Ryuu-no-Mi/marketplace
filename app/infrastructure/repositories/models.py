from sqlalchemy import Column, Integer, String, Float

from app.core.database import Base


class ProductModel(Base):
    """
    Modelo SQLAlchemy para la tabla de productos.
    
    Este es un detalle de infraestructura, separado de la entidad de dominio.
    El dominio no debe conocer de SQLAlchemy.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
