"""Репозиторий: Поставки FBS."""
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orders import FbsSupply


class FbsSuppliesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(FbsSupply))
        return result.scalar_one()

    async def get_filtered(
        self,
        done: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[FbsSupply]:
        query = select(FbsSupply)
        if done is not None:
            query = query.where(FbsSupply.done == done)
        query = query.order_by(FbsSupply.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())
