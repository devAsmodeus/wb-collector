"""Репозиторий: Склады продавца."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.products import WbWarehouse
from src.schemas.products.warehouses import SellerWarehouse


class WarehousesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, warehouses: list[SellerWarehouse]) -> int:
        """Вставляет или обновляет склады продавца."""
        if not warehouses:
            return 0
        rows = [
            {
                "warehouse_id": wh.id,
                "name": wh.name,
                "office_id": wh.officeId,
                "cargo_type": wh.cargoType,
                "delivery_type": wh.deliveryType,
                "is_deleting": wh.isDeleting,
                "is_processing": wh.isProcessing,
                "fetched_at": datetime.utcnow(),
            }
            for wh in warehouses if wh.id is not None
        ]
        if not rows:
            return 0
        stmt = insert(WbWarehouse).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["warehouse_id"],
            set_={k: getattr(stmt.excluded, k) for k in rows[0] if k != "warehouse_id"},
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(WbWarehouse))
        return result.scalar_one()

    async def get_all(self) -> list[WbWarehouse]:
        result = await self._session.execute(select(WbWarehouse).order_by(WbWarehouse.warehouse_id))
        return list(result.scalars().all())
