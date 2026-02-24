from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.domain.entities import Product
from app.domain.repositories import ProductRepository
from app.infrastructure.repositories.models import ProductModel


class SqlAlchemyProductRepository(ProductRepository):
    """
    Implementación de ProductRepository usando SQLAlchemy.
    
    Esta clase pertenece a la capa de infraestructura.
    El dominio no conoce de su existencia.
    """

    def __init__(self, session_factory):
        """
        Inicializa el repositorio con una sesión de SQLAlchemy.
        
        Args:
            session: Sesión de SQLAlchemy. Si no se proporciona, se usa SessionLocal.
        """
        self.session_factory = session_factory

    def add(self, product: Product) -> Product:
        """
        Persiste un nuevo producto en la base de datos.
        
        Args:
            product: Entidad de dominio Product.
            
        Returns:
            Product: El producto con el id asignado por la BD.
        """
        with self.session_factory() as session:
        # Convertir de entidad de dominio a modelo SQLAlchemy
            db_product = ProductModel(
                name=product.name,
                price=product.price,
                stock=product.stock,
                user_id=product.user_id,
                category_id=product.category_id,
                description=product.description,
                is_active=product.is_active
            )
        
            # Persistir
            self.session.add(db_product)
            self.session.commit()
            self.session.refresh(db_product)
        
            # Convertir de modelo SQLAlchemy de vuelta a entidad de dominio
            return self._to_domain(db_product)

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        Obtiene un producto por su id.
        
        Args:
            product_id: Identificador del producto (UUID).
            
        Returns:
            Optional[Product]: La entidad de dominio si existe, None si no.
        """
        with self.session_factory() as session:
            db_product = session.query(ProductModel).filter(
                ProductModel.id == product_id
            ).first()
        
        return self._to_domain(db_product) if db_product else None

    def list_all(self) -> List[Product]:
        """
        Obtiene todos los productos.
        
        Returns:
            List[Product]: Lista de entidades de dominio.
        """
        db_products = self.session.query(ProductModel).all()
        return [self._to_domain(db_product) for db_product in db_products]

    def _to_domain(self, db_product: ProductModel) -> Product:
        """
        Convierte un modelo SQLAlchemy a una entidad de dominio.
        
        Args:
            db_product: Modelo SQLAlchemy ProductModel.
            
        Returns:
            Product: Entidad de dominio.
        """
        return Product(
            id=db_product.id,
            name=db_product.name,
            price=float(db_product.price),
            stock=db_product.stock,
            user_id=db_product.user_id,
            category_id=db_product.category_id,
            description=db_product.description,
            is_active=db_product.is_active,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at
        )
