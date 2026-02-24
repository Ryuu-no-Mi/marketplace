from abc import ABC, abstractmethod
from typing import Optional,List
from uuid import UUID

from app.domain.entities import User

class UserRepository(ABC):
    """Puerto: define cómo acceder a Users."""

    @abstractmethod
    def add(self, user: User) -> User:
        """Crear usuario."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Obtener usuario por ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email."""
        pass

    @abstractmethod
    def list_all(self) -> List[User]:
        """Listar todos los usuarios."""
        pass
    
    @abstractmethod
    def get_active_users(self) -> List[User]:
        """Listar usuarios activos."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualizar usuario."""
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        """Eliminar usuario."""
        pass

    @abstractmethod
    def to_domain(self, db_user) -> User:
        """Convertir modelo de base de datos a entidad de dominio."""
        pass
    