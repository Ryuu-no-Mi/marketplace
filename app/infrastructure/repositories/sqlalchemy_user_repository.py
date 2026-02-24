from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.domain.entities import User
from app.domain.repositories import UserRepository
from app.infrastructure.repositories.models import UserModel


class SqlAlchemyUserRepository (UserRepository):
    """
    Implementación de UserRepository usando SQLAlchemy.
    
    Esta clase pertenece a la capa de infraestructura.
    El dominio no conoce de su existencia.
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, user: User) -> User:
        with self.session_factory() as session:
            user_model = UserModel(
                id=user.id,
                name=user.name,
                email=user.email,
                password_hash=user.password_hash,
                created_at=user.created_at
            )
            session.add(user_model)
            session.commit()
            session.refresh(user_model)
            return User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                password_hash=user_model.password_hash,
                created_at=user_model.created_at
            )

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        with self.session_factory() as session:
            db_user = session.query(UserModel).filter(
                UserModel.id == user_id
            ).first()
            return self.to_domain(db_user) if db_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        with self.session_factory() as session:
            db_user = session.query(UserModel).filter(
                UserModel.email == email
            ).first()
            return self.to_domain(db_user) if db_user else None

    def list_all(self) -> List[User]:
        with self.session_factory() as session:
            db_users = session.query(UserModel).all()
            return [self.to_domain(db_user) for db_user in db_users]

    def get_active_users(self) -> List[User]:
        with self.session_factory() as session:
            db_users = session.query(UserModel).filter(
                UserModel.is_active == True
            ).all()
            return [self.to_domain(db_user) for db_user in db_users]
            
    def update(self, user: User) -> User:
        with self.session_factory() as session:
            db_user = session.query(UserModel).filter(
                UserModel.id == user.id
            ).first()
            if not db_user:
                raise ValueError("Usuario no encontrado")
            db_user.name = user.name
            db_user.email = user.email
            db_user.password_hash = user.password_hash
            db_user.is_active = user.is_active
            session.commit()
            return self.to_domain(db_user)

    def delete(self, user_id: UUID) -> None:
        with self.session_factory() as session:
            db_user = session.query(UserModel).filter(
                UserModel.id == user_id
            ).first()

            if db_user:
                #session.delete(db_user) //vamos a hacer borrado lógico
                db_user.is_active = False
                session.commit()

    def to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password_hash=db_user.password_hash,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            is_active=db_user.is_active
        )