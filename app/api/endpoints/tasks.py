from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from app.api.schemas.tasks import CreateTask, TaskResponse, TaskDescription
from app.api.schemas.users import RegisterUser, UserResponse
from app.services.tasks_service import TasksService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork
from app.core.security import get_user_from_token

tasks_router = APIRouter()

async def get_tasks_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> TasksService:
    return TasksService(uow)


@tasks_router.post('/register', response_model=UserResponse)
async def registration(user: RegisterUser, task_service: TasksService = Depends(get_tasks_service)) -> UserResponse:
    # Создание нового пользователя с необходимыми данными
    return await task_service.register_user(user)


@tasks_router.post('/login')
async def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                task_service: TasksService = Depends(get_tasks_service)) -> dict:
    # Аутентификация пользователя и выдача JWT-токена
    jwt = await task_service.get_jwt(user_data)
    return {"access_token": jwt, "token_type": "bearer"}


@tasks_router.post('/logout')
async def logout() -> dict:
    # Инвалидизация JWT-токена пользователя
    pass


@tasks_router.post('/tasks', response_model=TaskResponse)
async def create_new_task(task: TaskDescription,
                          task_service: TasksService = Depends(get_tasks_service),
                          current_user: str = Depends(get_user_from_token)) -> TaskResponse:
    # Создание новой записи пользователя
    task_to_db = CreateTask(description=task.description, user=current_user)
    return await task_service.add_task(task_to_db)


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