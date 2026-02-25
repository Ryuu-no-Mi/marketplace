from datetime import date, datetime

from app.domain.entities import User
from app.domain.repositories import UserRepository


class CreateUser:
    """
    Caso de uso para crear un nuevo usuario.
    
    Utiliza inyección de dependencias para recibir el repositorio.
    No depende de detalles de infraestructura, solo de abstracciones del dominio.
    """

    def __init__(self, repository: UserRepository):
        """
        Inicializa el caso de uso con una instancia del repositorio.
        
        Args:
            repository: Implementación de UserRepository para persistir el usuario.
        """
        self.repository = repository

    def execute(
        self,
        email: str,
        password_hash: str,
        name: str,
        last_name: str,
        birth_date: date,
        role: str = "customer"
    ) -> User:
        """
        Ejecuta la creación de un nuevo usuario.
        
        Args:
            email: Email del usuario.
            password_hash: Hash de la contraseña.
            name: Nombre del usuario.
            last_name: Apellido del usuario.
            birth_date: Fecha de nacimiento del usuario.
            role: Rol del usuario (admin, seller, customer).
            
        Returns:
            User: El usuario creado y persistido.
            
        Raises:
            ValueError: Si los datos no cumplen con las reglas de negocio.
        """
        # Crear la entidad de dominio (se valida en User.__post_init__)
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            last_name=last_name,
            birth_date=birth_date,
            role=role,
            is_active=True
        )
        
        # Persistir usando el repositorio inyectado
        created_user = self.repository.add(user)
        
        return created_user