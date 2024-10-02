from abc import ABC, abstractmethod

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, data: dict):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        sql_query = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(sql_query)
        return res.scalar_one()

    async def find_all(self, data: dict):
        res = await self.session.execute(select(self.model))
        return res.scalars().all()

    async def get_one(self, filters: dict):
        sql_query = select(self.model).filter_by(**filters)
        res = await self.session.execute(sql_query)
        return res.scalar()