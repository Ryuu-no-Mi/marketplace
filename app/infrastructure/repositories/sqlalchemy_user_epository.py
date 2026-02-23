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


    def to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password_hash=db_user.password_hash,
            created_at=db_user.created_at
        )