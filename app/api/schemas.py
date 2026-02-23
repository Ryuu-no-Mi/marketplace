from pydantic import BaseModel, Field


class CreateProductRequest(BaseModel):
    """DTO para crear un producto."""
    name: str = Field(..., min_length=1, description="Nombre del producto")
    price: float = Field(..., gt=0, description="Precio del producto")


class ProductResponse(BaseModel):
    """DTO para responder información del producto."""
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True
