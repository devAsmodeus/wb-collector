"""Сервис Sync: Маркетинг — Синхронизация акций (календарь)."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.promotion.calendar import CalendarCollector
from src.repositories.promotion.promotions import PromotionsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class CalendarSyncService(BaseService):

    async def sync_promotions(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка акций из календаря WB.
        Загружает все акции через get_promotions и сохраняет в wb_promotions.
        """
        repo = PromotionsRepository(session)

        async with CalendarCollector() as collector:
            response = await collector.get_promotions()

        promotions = []
        if isinstance(response, list):
            promotions = response
        elif isinstance(response, dict):
            promotions = response.get("data", response.get("promotions", []))
            if not isinstance(promotions, list):
                promotions = [response]

        saved = await repo.upsert_many(promotions)
        logger.info(f"Promotions synced: {saved} promotions saved")
        return {"synced": saved, "source": "full"}
