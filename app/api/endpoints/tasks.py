from fastapi import APIRouter
from pygments.lexer import default

tasks_router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@tasks_router.post('/register')
async def registration() -> dict:
    # Создание нового пользователя с необходимыми данными
    pass


@tasks_router.post('/login')
async def login() -> dict:
    # Аутентификация пользователя и выдача JWT-токена
    pass


@tasks_router.post('/logout')
async def logout() -> dict:
    # Инвалидизация JWT-токена пользователя
    pass


@tasks_router.post('/tasks')
async def create_new_task() -> dict:
    # Создание новой записи пользователя
    pass


@tasks_router.get('/tasks')
async def get_all_tasks() -> dict:
    # Получение списка всех записей текущего пользователя
    pass


@tasks_router.get('/tasks/{task_id}')
async def get_task_by_id() -> dict:
    # Получение детали конкретной записи по её идентификатору
    pass


@tasks_router.put('/tasks/{task_id}')
async def update_task() -> dict:
    # Обновление данных конкретной записи
    pass


@tasks_router.delete('/tasks/{task_id}')
async def delete_task() -> dict:
    # Удаление конкретной записи
    pass