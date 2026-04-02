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
        Использует /adv/v1/promotion/count который возвращает все кампании
        с advertId, type, status, changeTime без необходимости батчевых запросов.
        """
        repo = CampaignsRepository(session)

        async with CampaignsCollector() as collector:
            count_response = await collector.get_count()

        # count_response.adverts — список групп по type+status
        # Каждая группа содержит advert_list с advertId и changeTime
        campaigns = []
        raw = count_response.model_dump() if hasattr(count_response, "model_dump") else {}
        for group in (raw.get("adverts") or []):
            advert_type = group.get("type")
            advert_status = group.get("status")
            for item in (group.get("advert_list") or []):
                if not item:
                    continue
                # advert_list может быть list[dict] или list[str] в зависимости от версии схемы
                if isinstance(item, str):
                    continue
                campaigns.append({
                    "advertId": item.get("advertId"),
                    "changeTime": item.get("changeTime"),
                    "type": advert_type,
                    "status": advert_status,
                    "name": None,
                    "paymentType": None,
                    "createTime": None,
                    "startTime": None,
                    "endTime": None,
                })

        if not campaigns:
            logger.warning("Campaigns: count endpoint returned no items")
            return {"synced": 0, "source": "full"}

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
