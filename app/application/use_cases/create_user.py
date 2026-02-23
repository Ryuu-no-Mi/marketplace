

class CreateUser:
    """
    Caso de uso para crear un nuevo usuario.
    """

    def __init__(self,repository: UserRepository):
        self.repository = repository

    def execute(self, name: str, email: str, password: str, last_name: str, birth_date: date, role: str) -> User:
        """Ejecuta la creación de un nuevo usuario."""

        user = User(name=name, email=email, password=password, last_name=last_name, birth_date=birth_date, role=role)
        
        created_user = self.repository.add(user)

        return created_user