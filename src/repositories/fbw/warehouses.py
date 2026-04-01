"""Репозиторий: Склады WB для FBW-поставок."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.fbw import FbwWarehouse


class FbwWarehousesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[dict]) -> int:
        """Вставляет или обновляет склады FBW. Возвращает кол-во обработанных записей."""
        if not items:
            return 0
        rows = [
            {
                "id": item["id"],
                "name": item.get("name"),
                "address": item.get("address"),
                "work_time": item.get("work_time"),
                "accepts_qr": item.get("accepts_qr"),
                "raw_data": item.get("raw_data"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(FbwWarehouse).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "name": stmt.excluded.name,
                "address": stmt.excluded.address,
                "work_time": stmt.excluded.work_time,
                "accepts_qr": stmt.excluded.accepts_qr,
                "raw_data": stmt.excluded.raw_data,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        """Возвращает общее количество складов FBW в БД."""
        result = await self._session.execute(select(func.count()).select_from(FbwWarehouse))
        return result.scalar_one()

    async def get_all(self, limit: int = 500, offset: int = 0) -> list[FbwWarehouse]:
        """Возвращает склады FBW с пагинацией."""
        result = await self._session.execute(
            select(FbwWarehouse).order_by(FbwWarehouse.id).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_id(self, warehouse_id: int) -> FbwWarehouse | None:
        """Возвращает склад по ID."""
        result = await self._session.execute(
            select(FbwWarehouse).where(FbwWarehouse.id == warehouse_id)
        )
        return result.scalars().one_or_none()
