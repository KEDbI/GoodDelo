from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from passlib.hash import pbkdf2_sha256

from sqlalchemy.exc import NoResultFound

from app.api.schemas.tasks import CreateTask, TaskResponse
from app.api.schemas.users import RegisterUser, UserResponse
from app.utils.unitofwork import IUnitOfWork
from app.core.security import create_jwt


class TasksService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def register_user(self, user: RegisterUser) -> UserResponse:
        async with self.uow:
            user_db = await self.uow.users.get_one({'login': user.login})
            if user_db:
                raise HTTPException(status_code=400, detail='This login already exists!')
            user.password = pbkdf2_sha256.hash(user.password)
            user_dict = user.model_dump()
            user_to_db = await self.uow.users.add_one(user_dict)
            user_response = UserResponse.model_validate(user_to_db)
            await self.uow.commit()
            return user_response

    async def get_jwt(self, user_data: OAuth2PasswordRequestForm) -> str:
        async with self.uow:
            user_db = await self.uow.users.get_one({'login': user_data.username})
            if user_db is None or not pbkdf2_sha256.verify(user_data.password, user_db.password):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid login or password",
                    headers={"WWW-Authenticate": "Bearer"})
            data_for_jwt = {'sub': user_db.login}
            return create_jwt(data_for_jwt)

    async def add_task(self, task: CreateTask) -> TaskResponse:
        async with self.uow:
            task_dict = task.model_dump()
            task_to_db = await self.uow.tasks.add_one(task_dict)
            task_response = TaskResponse.model_validate(task_to_db)
            await self.uow.commit()
            return task_response

    async def select_all_tasks(self, login: str) -> list:
        async with self.uow:
            tasks_from_db = await self.uow.tasks.find_all_with_filter({'user': login})
            res = [TaskResponse.model_validate(i) for i in tasks_from_db]
            return res

    async def select_task_by_id(self, task_id: int, login: str) -> TaskResponse:
        async with self.uow:
            task_from_db = await self.uow.tasks.get_one({'user': login,
                                                         'id': task_id})
            if task_from_db:
                task_response = TaskResponse.model_validate(task_from_db)
                return task_response
            raise HTTPException(status_code=403, detail='Wrong task_id')

    async def update_task_by_id(self, task_id: int, login: str, updates: dict) -> TaskResponse:
        async with self.uow:
            try:
                update_db = await self.uow.tasks.update_one(filters={'id': task_id,
                                                                 'user': login},
                                                        data=updates)
                task_response = TaskResponse.model_validate(update_db)
                await self.uow.commit()
                return task_response
            except NoResultFound:
                # NoResultFound выпадает, если по login и task_id в бд не найдено строк
                # (соответственно, если авторизованный пользователь ввел task_id другого пользователя,
                # то выпадет эта ошибка)
                raise HTTPException(status_code=403, detail='Wrong task_id')

    async def del_task_by_id(self, task_id: int, login:str) -> TaskResponse:
        async with self.uow:
            try:
                del_task = await self.uow.tasks.delete_one(filters={'id': task_id,
                                                                 'user': login})
                task_response = TaskResponse.model_validate(del_task)
                await self.uow.commit()
                return task_response
            except NoResultFound:
                # NoResultFound выпадает, если по login и task_id в бд не найдено строк
                # (соответственно, если авторизованный пользователь ввел task_id другого пользователя,
                # то выпадет эта ошибка)
                raise HTTPException(status_code=403, detail='Wrong task_id')







