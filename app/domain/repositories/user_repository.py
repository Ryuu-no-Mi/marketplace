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
    
    