from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime
from uuid import UUID


@dataclass
class User:
    """
    Entidad de dominio que representa un usuario.
    No tiene dependencias de frameworks externos (FastAPI, SQLAlchemy).
    Solo tipos Python puros.
    """
    email: str
    password_hash: str
    name: str
    last_name: str
    birth_date: date
    role: str
    id: Optional[UUID] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones básicas de dominio."""
        if not self.email or not isinstance(self.email, str) or "@" not in self.email:
            raise ValueError("El correo electrónico es requerido y debe ser válido")
        
        if not self.password_hash or not isinstance(self.password_hash, str):
            raise ValueError("El hash de contraseña es requerido y debe ser texto")
        
        if not self.name or not isinstance(self.name, str):
            raise ValueError("El nombre es requerido y debe ser texto")
        
        if not self.last_name or not isinstance(self.last_name, str):
            raise ValueError("El apellido es requerido y debe ser texto")
        
        if not isinstance(self.birth_date, date):
            raise ValueError("La fecha de nacimiento debe ser una fecha válida")
        
        if self.role not in ('admin', 'seller', 'customer'):
            raise ValueError("El rol debe ser 'admin', 'seller' o 'customer'")
        
        if not isinstance(self.is_active, bool):
            raise ValueError("is_active debe ser un valor booleano")
