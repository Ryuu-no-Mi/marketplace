from app.domain.entities import Product
from app.domain.repositories import ProductRepository


class CreateProduct:
    """
    Caso de uso para crear un nuevo producto.
    
    Utiliza inyección de dependencias para recibir el repositorio.
    No depende de detalles de infraestructura, solo de abstracciones del dominio.
    """

    def __init__(self, repository: ProductRepository):
        """
        Inicializa el caso de uso con una instancia del repositorio.
        
        Args:
            repository: Implementación de ProductRepository para persistir el producto.
        """
        self.repository = repository

    def execute(self, name: str, price: float) -> Product:
        """
        Ejecuta la creación de un nuevo producto.
        
        Args:
            name: Nombre del producto.
            price: Precio del producto.
            
        Returns:
            Product: El producto creado y persistido.
            
        Raises:
            ValueError: Si los datos no cumplen con las reglas de negocio.
        """
        # Crear la entidad de dominio (se valida en Product.__post_init__)
        product = Product(name=name, price=price)
        
        # Persistir usando el repositorio inyectado
        created_product = self.repository.add(product)
        
        return created_product
