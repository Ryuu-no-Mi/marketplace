from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Literal, Optional
from datetime import date
from uuid import UUID
import re


class CreateProductRequest(BaseModel):
    """DTO para crear un producto."""
    name: str = Field(..., min_length=1, description="Nombre del producto")
    price: float = Field(..., gt=0, description="Precio del producto")
    stock: int = Field(..., ge=0, description="Cantidad en stock del producto")
    seller_id: UUID = Field(..., description="ID del vendedor (UUID)")
    category_id: Optional[UUID] = Field(None, description="ID de la categoría (UUID)")
    description: Optional[str] = Field(None, description="Descripción del producto")
    
    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    """DTO para responder información del producto."""
    id: UUID
    name: str
    price: float
    stock: int
    seller_id: UUID
    category_id: Optional[UUID] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):
    """DTO para crear un usuario."""
    name: str = Field(..., min_length=1, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(
        ..., 
        min_length=8,
        description="Contraseña del usuario (mínimo 8 caracteres: minúscula, mayúscula, número y especial)"
    )
    last_name: str = Field(..., min_length=1, description="Apellido del usuario")
    birth_date: date = Field(..., description="Fecha de nacimiento del usuario (YYYY-MM-DD)")
    role: Literal["admin", "seller", "customer"] = Field(..., description="Rol del usuario: admin, seller o customer")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Valida que la contraseña cumpla con los requisitos:
        - Mínimo 8 caracteres
        - Al menos una letra minúscula
        - Al menos una letra mayúscula
        - Al menos un dígito
        - Al menos un carácter especial (@$!%*?&)
        """
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe contener al menos una letra minúscula")
        
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe contener al menos un número")
        
        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("La contraseña debe contener al menos un carácter especial (@$!%*?&)")
        
        return v

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """DTO para responder información del usuario."""
    id: UUID
    email: str
    name: str
    last_name: str
    birth_date: date
    role: str
    is_active: bool

    class Config:
        from_attributes = True
