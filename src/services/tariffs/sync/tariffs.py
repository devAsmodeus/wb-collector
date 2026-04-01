"""Сервис Sync: Тарифы — Синхронизация тарифов WB в БД."""
import logging
from datetime import date

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
        items = response.report or []
        saved = await repo.upsert_commissions(items)
        logger.info(f"Tariff commissions synced: {saved} records")
        return {"synced": saved, "source": "commissions"}

    async def sync_box_tariffs(self, session: AsyncSession) -> dict:
        """Загружает тарифы коробами и сохраняет в БД."""
        repo = TariffsRepository(session)
        today = date.today().isoformat()
        async with TariffsCollector() as collector:
            response = await collector.get_box_tariffs(date=today)
        items = response.warehouseList or []
        saved = await repo.upsert_box_tariffs(items)
        logger.info(f"Tariff box synced: {saved} records")
        return {"synced": saved, "source": "box"}

    async def sync_pallet_tariffs(self, session: AsyncSession) -> dict:
        """Загружает тарифы паллетами и сохраняет в БД."""
        repo = TariffsRepository(session)
        today = date.today().isoformat()
        async with TariffsCollector() as collector:
            response = await collector.get_pallet_tariffs(date=today)
        items = response.warehouseList or []
        saved = await repo.upsert_pallet_tariffs(items)
        logger.info(f"Tariff pallet synced: {saved} records")
        return {"synced": saved, "source": "pallet"}

    async def sync_supply_tariffs(self, session: AsyncSession) -> dict:
        """Загружает коэффициенты приёмки и сохраняет в БД."""
        repo = TariffsRepository(session)
        async with TariffsCollector() as collector:
            items = await collector.get_supply_tariffs()
        saved = await repo.upsert_supply_tariffs(items)
        logger.info(f"Tariff supply synced: {saved} records")
        return {"synced": saved, "source": "supply"}
