from abc import ABC, abstractmethod
from sqlalchemy import insert, select, func, asc, desc
from typing import Optional, List
from sqlalchemy.exc import NoResultFound
from src.core.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError


class PostgresRepository(AbstractRepository):

    model = None

    async def add_one(self, data: dict) -> dict:
        if "image" in data and not isinstance(data["image"], str):
            data["image"] = str(data["image"])

        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
            
    
    async def get_all(self, skip: int = 0, limit: int = 10):
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        products = result.scalars().all()

        total_query = select(func.count()).select_from(self.model)
        total = (await self.session.execute(total_query)).scalar_one()

        return products, total
        
    async def get_one(self, id: int) -> Optional[dict]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            return obj.to_read_model() if obj else None