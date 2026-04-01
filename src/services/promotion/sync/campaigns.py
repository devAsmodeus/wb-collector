"""Сервис Sync: Маркетинг — Синхронизация кампаний."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.promotion.campaigns import CampaignsCollector
from src.repositories.promotion.campaigns import CampaignsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class CampaignsSyncService(BaseService):

    async def sync_campaigns(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех рекламных кампаний.
        Загружает кампании через get_adverts и сохраняет в wb_campaigns.
        """
        repo = CampaignsRepository(session)

        async with CampaignsCollector() as collector:
            response = await collector.get_adverts()

        campaigns = []
        if isinstance(response, list):
            campaigns = response
        elif isinstance(response, dict):
            campaigns = response.get("adverts", response.get("data", []))
            if not isinstance(campaigns, list):
                campaigns = [response]

        saved = await repo.upsert_many(campaigns)
        logger.info(f"Campaigns synced: {saved} campaigns saved")
        return {"synced": saved, "source": "full"}

    async def sync_campaigns_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация кампаний.
        Кампании могут изменяться в любой момент, поэтому incremental = full sync.
        """
        result = await self.sync_campaigns(session)
        result["source"] = "incremental"
        return result
