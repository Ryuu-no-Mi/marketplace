from pydantic import BaseModel, Field, EmailStr
from typing import Literal
from datetime import date
from uuid import UUID


class CreateProductRequest(BaseModel):
    """DTO para crear un producto."""
    name: str = Field(..., min_length=1, description="Nombre del producto")
    price: float = Field(..., gt=0, description="Precio del producto")
    stock: int = Field(..., ge=0, description="Cantidad en stock del producto")
    user_id: UUID = Field(..., description="ID del vendedor (UUID)")
    category_id: Optional[UUID] = Field(None, description="ID de la categoría (UUID)")
    description: Optional[str] = Field(None, description="Descripción del producto")
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    """DTO para responder información del producto."""
    id: UUID
    name: str
    price: float

    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):
    """DTO para crear un usuario."""
    name: str = Field(..., min_length=1, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(
        ..., 
        min_length=8,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Contraseña del usuario (mínimo 8 caracteres, con minúscula, mayúscula, número y carácter especial)"
    )
    last_name: str = Field(..., min_length=1, description="Apellido del usuario")
    birth_date: date = Field(..., description="Fecha de nacimiento del usuario (YYYY-MM-DD)")
    role: Literal["admin", "seller", "customer"] = Field(..., description="Rol del usuario: admin, seller o customer")

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
