from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities import Product


class ProductRepository(ABC):
    """
    Interfaz de repositorio para la entidad Product.
    Invierte la dependencia: las implementaciones dependen de esta abstracción.
    
    Esto permite cambiar la persistencia sin afectar el dominio.
    """

    @abstractmethod
    def add(self, product: Product) -> Product:
        """
        Añade un nuevo producto al repositorio.
        
        Args:
            product: Instancia de Product a persistir.
            
        Returns:
            Product: El producto persistido (con id asignado).
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        Obtiene un producto por su id.
        
        Args:
            product_id: Identificador del producto (UUID).
            
        Returns:
            Optional[Product]: El producto si existe, None si no.
        """
        pass

    @abstractmethod
    def list_all(self) -> List[Product]:
        """
        Obtiene todos los productos.
        
        Returns:
            List[Product]: Lista de productos.
        """
        pass
