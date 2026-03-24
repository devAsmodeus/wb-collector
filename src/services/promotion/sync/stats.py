"""Сервис Sync: Маркетинг — Синхронизация статистики кампаний."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.promotion.campaigns import CampaignsCollector
from src.collectors.promotion.stats import StatsCollector
from src.repositories.promotion.campaign_stats import CampaignStatsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class StatsSyncService(BaseService):

    async def sync_stats(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка статистики по всем кампаниям.
        Сначала получает список активных кампаний, затем запрашивает fullstats
        батчами по 50 кампаний и сохраняет в wb_campaign_stats.
        """
        repo = CampaignStatsRepository(session)

        # Получаем список кампаний
        async with CampaignsCollector() as collector:
            response = await collector.get_adverts()

        campaign_ids = []
        if isinstance(response, list):
            for c in response:
                if isinstance(c, dict) and c.get("advertId"):
                    campaign_ids.append(c["advertId"])
        elif isinstance(response, dict):
            adverts = response.get("adverts", response.get("data", []))
            if isinstance(adverts, list):
                for c in adverts:
                    if isinstance(c, dict) and c.get("advertId"):
                        campaign_ids.append(c["advertId"])

        if not campaign_ids:
            return {"synced": 0, "source": "full", "message": "No campaigns found"}

        total_saved = 0

        # Запрашиваем статистику батчами по 50 кампаний
        async with StatsCollector() as collector:
            for i in range(0, len(campaign_ids), 50):
                batch_ids = campaign_ids[i:i + 50]
                ids_str = ",".join(str(cid) for cid in batch_ids)

                try:
                    response = await collector.get_fullstats(ids_str)
                except Exception as e:
                    logger.warning(f"Failed to get fullstats for batch {i}: {e}")
                    continue

                stats = []
                if isinstance(response, list):
                    for item in response:
                        advert_id = item.get("advertId")
                        days = item.get("days", [])
                        for day in days:
                            stats.append({
                                "advert_id": advert_id,
                                "date": day.get("date"),
                                "views": day.get("views"),
                                "clicks": day.get("clicks"),
                                "ctr": day.get("ctr"),
                                "cpc": day.get("cpc"),
                                "sum": day.get("sum"),
                                "atbs": day.get("atbs"),
                                "orders": day.get("orders"),
                                "cr": day.get("cr"),
                                "shks": day.get("shks"),
                                "sum_price": day.get("sum_price"),
                                "raw_data": day,
                            })
                elif isinstance(response, dict):
                    data = response.get("data", [])
                    if isinstance(data, list):
                        for item in data:
                            advert_id = item.get("advertId")
                            days = item.get("days", [])
                            for day in days:
                                stats.append({
                                    "advert_id": advert_id,
                                    "date": day.get("date"),
                                    "views": day.get("views"),
                                    "clicks": day.get("clicks"),
                                    "ctr": day.get("ctr"),
                                    "cpc": day.get("cpc"),
                                    "sum": day.get("sum"),
                                    "atbs": day.get("atbs"),
                                    "orders": day.get("orders"),
                                    "cr": day.get("cr"),
                                    "shks": day.get("shks"),
                                    "sum_price": day.get("sum_price"),
                                    "raw_data": day,
                                })

                if stats:
                    saved = await repo.upsert_many(stats)
                    total_saved += saved

        logger.info(f"Campaign stats synced: {total_saved} stats saved")
        return {"synced": total_saved, "campaigns": len(campaign_ids), "source": "full"}
