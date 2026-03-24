"""Репозиторий: Склады продавца."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.products import WbWarehouse
from src.schemas.products.warehouses import SellerWarehouse


class WarehousesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, warehouses: list[SellerWarehouse]) -> int:
        """Вставляет или обновляет склады продавца. Возвращает кол-во обработанных записей."""
        if not warehouses:
            return 0
        rows = [
            {
                "warehouse_id": wh.warehouseId or wh.id,
                "name": wh.name,
                "address": None,
                "work_time": None,
                "selected_coefficient": None,
                "fetched_at": datetime.utcnow(),
            }
            for wh in warehouses
        ]
        stmt = insert(WbWarehouse).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["warehouse_id"],
            set_={
                "name": stmt.excluded.name,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self) -> list[WbWarehouse]:
        """Возвращает все склады продавца."""
        result = await self._session.execute(
            select(WbWarehouse).order_by(WbWarehouse.warehouse_id)
        )
        return list(result.scalars().all())
