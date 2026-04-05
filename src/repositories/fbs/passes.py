"""Репозиторий: Пропуска FBS."""
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orders import FbsPass


class FbsPassesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(FbsPass))
        return result.scalar_one()

    async def get_filtered(
        self,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[FbsPass]:
        query = select(FbsPass)
        if status:
            query = query.where(FbsPass.status == status)
        query = query.order_by(FbsPass.date_start.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())
