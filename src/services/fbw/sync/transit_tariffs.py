"""Сервис Sync: FBW — Синхронизация тарифов транзитной доставки."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.fbw.acceptance import FBWAcceptanceCollector
from src.repositories.fbw.transit_tariffs import FbwTransitTariffsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class FbwTransitTariffsSyncService(BaseService):

    async def sync_transit_tariffs_full(self, session: AsyncSession) -> dict:
        """Полная выгрузка тарифов транзитной доставки FBW."""
        repo = FbwTransitTariffsRepository(session)

        async with FBWAcceptanceCollector() as collector:
            response = await collector.get_transit_tariffs()

        tariffs = response.tariffs or []
        items = [
            {
                "transit_warehouse_name": t.transitWarehouseName,
                "destination_warehouse_name": t.destinationWarehouseName,
                "active_from": t.activeFrom,
                "box_tariff": [bt.model_dump() for bt in t.boxTariff] if t.boxTariff else None,
                "pallet_tariff": t.palletTariff,
                "raw_data": t.model_dump(),
            }
            for t in tariffs
            if t.transitWarehouseName and t.destinationWarehouseName
        ]

        saved = await repo.upsert_many(items)
        logger.info(f"FBW transit tariffs synced: {saved} tariffs saved")
        return {"synced": saved, "source": "full"}

    async def sync_transit_tariffs_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация тарифов транзита FBW.
        Тарифы — справочные данные, incremental = full sync.
        """
        result = await self.sync_transit_tariffs_full(session)
        result["source"] = "incremental"
        return result
