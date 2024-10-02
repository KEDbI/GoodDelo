from app.db.models import Users
from app.repositories.base_repository import Repository

class UsersRepository(Repository):
    model = Users