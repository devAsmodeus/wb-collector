"""Сервис DB: FBW — Чтение тарифов транзитной доставки из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.fbw.transit_tariffs import FbwTransitTariffsRepository
from src.services.base import BaseService


class FbwTransitTariffsDbService(BaseService):

    async def get_transit_tariffs(
        self, session: AsyncSession, limit: int = 500, offset: int = 0,
    ) -> dict:
        """Возвращает тарифы транзитной доставки FBW из БД с пагинацией."""
        repo = FbwTransitTariffsRepository(session)
        total = await repo.count()
        items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "transit_warehouse_name": t.transit_warehouse_name,
                    "destination_warehouse_name": t.destination_warehouse_name,
                    "active_from": t.active_from,
                    "box_tariff": t.box_tariff,
                    "pallet_tariff": t.pallet_tariff,
                    "fetched_at": t.fetched_at.isoformat() if t.fetched_at else None,
                }
                for t in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
