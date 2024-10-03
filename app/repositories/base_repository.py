from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all_with_filter(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, filters: dict, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, filters: dict):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        sql_query = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(sql_query)
        return res.scalar_one()

    async def find_all_with_filter(self, data: dict):
        res = await self.session.execute(select(self.model).filter_by(**data))
        return res.scalars().all()

    async def get_one(self, filters: dict):
        sql_query = select(self.model).filter_by(**filters)
        res = await self.session.execute(sql_query)
        return res.scalar()

    async def update_one(self, filters: dict, data: dict):
        # Выражение с where выглядит, как костыль, но ничего лучше я не смог придумать
        sql_query = update(self.model).where((self.model.user == filters['user'])&(self.model.id == filters['id'])).values(**data).returning(self.model)
        res = await self.session.execute(sql_query)
        return res.scalar_one()

    async def delete_one(self, filters: dict):
        # Выражение с where выглядит, как костыль, но ничего лучше я не смог придумать
        sql_query = delete(self.model).where((self.model.user == filters['user'])&(self.model.id == filters['id'])).returning(self.model)
        res = await self.session.execute(sql_query)
        return res.scalar_one()