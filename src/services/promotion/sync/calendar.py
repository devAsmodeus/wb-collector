"""Сервис Sync: Промо-Календарь — синхронизация акций (ежедневная)."""
import logging
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.promotion.calendar import CalendarCollector
from src.repositories.promotion.promotions import PromotionsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class CalendarSyncService(BaseService):

    async def sync_promotions(self, session: AsyncSession) -> dict:
        """
        Полная синхронизация акций из календаря WB.
        Запрашивает все акции за диапазон -30/+180 дней.
        """
        repo = PromotionsRepository(session)

        now = datetime.utcnow()
        start = (now - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")
        end = (now + timedelta(days=180)).strftime("%Y-%m-%dT23:59:59Z")
        params = {
            "startDateTime": start,
            "endDateTime": end,
            "allPromo": "true",
            "limit": 1000,
            "offset": 0,
        }

        async with CalendarCollector() as collector:
            response = await collector.get_promotions(params=params)

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

    async def sync_promotions_incremental(self, session: AsyncSession) -> dict:
        """Акции — динамические данные, incremental = full sync."""
        result = await self.sync_promotions(session)
        result["source"] = "incremental"
        return result
