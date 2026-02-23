from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """
    Entidad de dominio que representa un producto.
    No tiene dependencias de frameworks externos (FastAPI, SQLAlchemy).
    """
    name: str
    price: float
    id: Optional[int] = None

    def __post_init__(self):
        """Validaciones básicas de dominio."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("El nombre del producto es requerido y debe ser texto")
        
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a cero")
