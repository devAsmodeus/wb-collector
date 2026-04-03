"""Сервис Sync: Маркетинг — Синхронизация статистики кампаний."""
import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.promotion.stats import StatsCollector
from src.repositories.promotion.campaign_stats import CampaignStatsRepository
from src.repositories.promotion.campaigns import CampaignsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)

# WB rate limit: 1 запрос/минута для /adv/v3/fullstats
FULLSTATS_RATE_LIMIT_DELAY = 61  # секунд между батчами
BATCH_SIZE = 50                  # макс IDs в одном запросе (лимит WB)
MAX_DATE_RANGE_DAYS = 14         # безопасный диапазон (WB лимит 20 дней)


class StatsSyncService(BaseService):

    async def sync_stats(
        self,
        session: AsyncSession,
        begin_date: str | None = None,
        end_date: str | None = None,
    ) -> dict:
        """
        Загружает статистику по всем рекламным кампаниям из БД.
        ВНИМАНИЕ: Rate limit WB — 1 запрос/минута. 1113 кампаний = ~23 минуты.
        Запускать через Celery task, не через HTTP.
        """
        repo = CampaignStatsRepository(session)
        campaigns_repo = CampaignsRepository(session)
        campaign_ids = await campaigns_repo.get_all_ids()

        if not campaign_ids:
            return {
                "synced": 0,
                "source": "full",
                "message": "No campaigns in DB — run /promotion/sync/campaigns/full first",
            }

        if not begin_date:
            begin_date = (datetime.utcnow() - timedelta(days=MAX_DATE_RANGE_DAYS)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.utcnow().strftime("%Y-%m-%d")

        total_batches = (len(campaign_ids) + BATCH_SIZE - 1) // BATCH_SIZE
        logger.info(
            f"Campaign stats: {len(campaign_ids)} campaigns, "
            f"{total_batches} batches, {begin_date}→{end_date}"
        )
        total_saved = 0

        async with StatsCollector() as collector:
            for batch_num, i in enumerate(range(0, len(campaign_ids), BATCH_SIZE), 1):
                batch_ids = campaign_ids[i : i + BATCH_SIZE]
                ids_str = ",".join(str(cid) for cid in batch_ids)

                # Rate limit: ждём перед каждым батчем кроме первого
                if batch_num > 1:
                    logger.info(f"Campaign stats: rate limit pause {FULLSTATS_RATE_LIMIT_DELAY}s before batch {batch_num}/{total_batches}")
                    await asyncio.sleep(FULLSTATS_RATE_LIMIT_DELAY)

                try:
                    response = await collector.get_fullstats(
                        ids_str,
                        begin_date=begin_date,
                        end_date=end_date,
                    )
                except Exception as e:
                    logger.warning(f"Campaign stats: batch {batch_num} failed — {e}")
                    continue

                stats = []
                # response — Pydantic модель FullStatsResponse с полем data
                if hasattr(response, "data"):
                    items = response.data or []
                elif isinstance(response, list):
                    items = response
                else:
                    items = []
                for item in items:
                    advert_id = item.get("advertId")
                    for day in (item.get("days") or []):
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
                    logger.info(f"Campaign stats: batch {batch_num}/{total_batches} → {saved} records, total={total_saved}")

        logger.info(f"Campaign stats synced: {total_saved} records total")
        return {"synced": total_saved, "campaigns": len(campaign_ids), "source": "full"}

    async def sync_stats_incremental(self, session: AsyncSession) -> dict:
        result = await self.sync_stats(session)
        result["source"] = "incremental"
        return result
