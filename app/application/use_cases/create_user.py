

class CreateUser:
    """
    Caso de uso para crear un nuevo usuario.
    """

    def __init__(self,repository: UserRepository):
        self.repository = repository

    def execute(self, name: str, email: str, password: str, last_name: str, birth_date: date, role: str) -> User:
        """Ejecuta la creación de un nuevo usuario."""

        user = User(id=None,email=email, password_hash=password, name=name, last_name=last_name, birth_date=birth_date, role=role, is_active=True, created_at=datetime.utcnow(), updated_at=None)
        
        created_user = self.repository.add(user)

        return created_user