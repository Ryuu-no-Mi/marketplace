from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID


@dataclass
class Product:
    """
    Entidad de dominio que representa un producto.
    No tiene dependencias de frameworks externos (FastAPI, SQLAlchemy).
    Solo tipos Python puros.
    """
    name: str
    price: float
    stock: int
    user_id: UUID
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    is_active: bool = True
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones básicas de dominio."""
        if not self.name or not isinstance(self.name, str) or len(self.name.strip()) == 0:
            raise ValueError("El nombre del producto es requerido y debe ser texto no vacío")
        
        if not isinstance(self.price, (int, float)):
            raise ValueError("El precio debe ser un número")
        
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a cero")
        
        if not isinstance(self.stock, int):
            raise ValueError("El stock debe ser un número entero")
        
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        if not isinstance(self.user_id, UUID):
            raise ValueError("El ID del vendedor debe ser un UUID válido")
        
        if self.category_id is not None and not isinstance(self.category_id, UUID):
            raise ValueError("El ID de la categoría debe ser un UUID válido")
        
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("La descripción debe ser texto")
        
        if not isinstance(self.is_active, bool):
            raise ValueError("is_active debe ser un valor booleano")
