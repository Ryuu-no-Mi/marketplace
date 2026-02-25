from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from app.api.schemas import CreateUserRequest, UserResponse
from app.application.use_cases import CreateUser
from app.infrastructure.repositories import SqlAlchemyUserRepository
from app.domain.repositories import UserRepository


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Usuario no encontrado"}},
)


def get_user_repository() -> UserRepository:
    """
    Inyección de dependencia para el repositorio de usuarios.
    Retorna una instancia de la implementación SQLAlchemy.
    """
    return SqlAlchemyUserRepository()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    request: CreateUserRequest,
    repository: UserRepository = Depends(get_user_repository),
):
    """
    Crea un nuevo usuario.
    
    No accede directamente a la base de datos.
    Utiliza el caso de uso CreateUser que orquesta la lógica.
    
    Args:
        request: Datos del usuario a crear (nombre, email, password, etc)
        repository: Repositorio inyectado por FastAPI
    
    Returns:
        UserResponse con los datos del usuario creado
    
    Raises:
        HTTPException 400: Si los datos no cumplen validaciones de dominio
        HTTPException 409: Si el email ya existe
    """
    try:
        # Inyectar el repositorio en el caso de uso
        create_user_use_case = CreateUser(repository)
        
        # Ejecutar el caso de uso
        user = create_user_use_case.execute(
            email=request.email,
            password_hash=request.password,
            name=request.name,
            last_name=request.last_name,
            birth_date=request.birth_date,
            role=request.role
        )
        
        # Convertir la entidad de dominio a DTO de respuesta
        return UserResponse(**user.__dict__)
    except ValueError as e:
        # Errores de validación de dominio
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Email duplicado u otros errores de BD
        if "unique constraint" in str(e).lower() or "email" in str(e).lower():
            raise HTTPException(status_code=409, detail="El email ya está registrado")
        raise HTTPException(status_code=500, detail="Error al crear el usuario")


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    repository: UserRepository = Depends(get_user_repository),
):
    """
    Obtiene un usuario por su ID.
    
    Args:
        user_id: ID del usuario a obtener
        repository: Repositorio inyectado por FastAPI
    
    Returns:
        UserResponse con los datos del usuario
    
    Raises:
        HTTPException 404: Si el usuario no existe
    """
    user = repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return UserResponse(**user.__dict__)


@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(
    email: str,
    repository: UserRepository = Depends(get_user_repository),
):
    """
    Obtiene un usuario por su email.
    
    Args:
        email: Email del usuario a buscar
        repository: Repositorio inyectado por FastAPI
    
    Returns:
        UserResponse con los datos del usuario
    
    Raises:
        HTTPException 404: Si el usuario no existe
    """
    user = repository.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return UserResponse(**user.__dict__)
