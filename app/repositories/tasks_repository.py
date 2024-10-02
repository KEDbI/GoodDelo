from app.db.models import Tasks
from app.repositories.base_repository import Repository

class TasksRepository(Repository):
    model = Tasks