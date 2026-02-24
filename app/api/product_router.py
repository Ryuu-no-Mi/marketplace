from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.api.schemas import CreateProductRequest, ProductResponse
from app.application.use_cases import CreateProduct
from app.infrastructure.repositories import SqlAlchemyProductRepository
from app.domain.repositories import ProductRepository


router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Producto no encontrado"}},
)


def get_product_repository() -> ProductRepository:
    """
    Inyección de dependencia para el repositorio de productos.
    Retorna una instancia de la implementación SQLAlchemy.
    """
    return SqlAlchemyProductRepository()


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    request: CreateProductRequest,
    repository: ProductRepository = Depends(get_product_repository),
):
    """
    Crea un nuevo producto.
    
    No accede directamente a la base de datos.
    Utiliza el caso de uso CreateProduct que orquesta la lógica.
    """
    try:
        # Inyectar el repositorio en el caso de uso
        create_product_use_case = CreateProduct(repository)
        
        # Ejecutar el caso de uso
        product = create_product_use_case.execute(
            name=request.name,
            price=request.price
        )
        
        # Convertir la entidad de dominio a DTO de respuesta
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price
        )
    except ValueError as e:
        # Errores de validación de dominio
        raise HTTPException(status_code=400, detail=str(e))
