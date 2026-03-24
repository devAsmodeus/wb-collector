"""Сервис Sync: Тарифы — Синхронизация тарифов WB в БД."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.tariffs.tariffs import TariffsCollector
from src.repositories.tariffs.tariffs import TariffsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class TariffsSyncService(BaseService):

    async def sync_commissions(self, session: AsyncSession) -> dict:
        """Загружает комиссии по категориям и сохраняет в БД."""
        repo = TariffsRepository(session)
        async with TariffsCollector() as collector:
            response = await collector.get_commissions()
        items = response.get("report", []) if isinstance(response, dict) else response
        if isinstance(items, list):
            saved = await repo.upsert_commissions(items)
        else:
            saved = 0
        logger.info(f"Tariff commissions synced: {saved} records")
        return {"synced": saved, "source": "commissions"}

    async def sync_box_tariffs(self, session: AsyncSession) -> dict:
        """Загружает тарифы коробами и сохраняет в БД."""
        repo = TariffsRepository(session)
        async with TariffsCollector() as collector:
            response = await collector.get_box_tariffs()
        items = response.get("response", {}).get("data", {}).get("warehouseList", []) if isinstance(response, dict) else response
        if isinstance(items, list):
            saved = await repo.upsert_box_tariffs(items)
        else:
            saved = 0
        logger.info(f"Tariff box synced: {saved} records")
        return {"synced": saved, "source": "box"}

    async def sync_pallet_tariffs(self, session: AsyncSession) -> dict:
        """Загружает тарифы паллетами и сохраняет в БД."""
        repo = TariffsRepository(session)
        async with TariffsCollector() as collector:
            response = await collector.get_pallet_tariffs()
        items = response.get("response", {}).get("data", {}).get("warehouseList", []) if isinstance(response, dict) else response
        if isinstance(items, list):
            saved = await repo.upsert_pallet_tariffs(items)
        else:
            saved = 0
        logger.info(f"Tariff pallet synced: {saved} records")
        return {"synced": saved, "source": "pallet"}

    async def sync_supply_tariffs(self, session: AsyncSession) -> dict:
        """Загружает коэффициенты поставок и сохраняет в БД."""
        repo = TariffsRepository(session)
        async with TariffsCollector() as collector:
            response = await collector.get_supply_tariffs()
        items = response if isinstance(response, list) else []
        saved = await repo.upsert_supply_tariffs(items)
        logger.info(f"Tariff supply synced: {saved} records")
        return {"synced": saved, "source": "supply"}
