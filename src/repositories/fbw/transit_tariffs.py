"""Репозиторий: Тарифы транзитной доставки FBW."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.fbw import FbwTransitTariff


class FbwTransitTariffsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[dict]) -> int:
        """Вставляет или обновляет тарифы транзита. Возвращает кол-во обработанных записей."""
        if not items:
            return 0
        rows = [
            {
                "transit_warehouse_name": item["transit_warehouse_name"],
                "destination_warehouse_name": item["destination_warehouse_name"],
                "active_from": item.get("active_from"),
                "box_tariff": item.get("box_tariff"),
                "pallet_tariff": item.get("pallet_tariff"),
                "raw_data": item.get("raw_data"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(FbwTransitTariff).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_fbw_transit_tariff_route",
            set_={
                "active_from": stmt.excluded.active_from,
                "box_tariff": stmt.excluded.box_tariff,
                "pallet_tariff": stmt.excluded.pallet_tariff,
                "raw_data": stmt.excluded.raw_data,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        """Возвращает общее количество тарифов транзита в БД."""
        result = await self._session.execute(select(func.count()).select_from(FbwTransitTariff))
        return result.scalar_one()

    async def get_all(self, limit: int = 500, offset: int = 0) -> list[FbwTransitTariff]:
        """Возвращает тарифы транзита с пагинацией."""
        result = await self._session.execute(
            select(FbwTransitTariff)
            .order_by(FbwTransitTariff.transit_warehouse_name)
            .limit(limit).offset(offset)
        )
        return list(result.scalars().all())
