"""Ð¡ÐµÑ€Ð²Ð¸Ñ Sync: ÐšÐ¾Ð¼Ð¼ÑƒÐ½Ð¸ÐºÐ°Ñ†Ð¸Ð¸ â€” Ð¡Ð¸Ð½Ñ…Ñ€Ð¾Ð½Ð¸Ð·Ð°Ñ†Ð¸Ñ Ð¾Ñ‚Ð·Ñ‹Ð²Ð¾Ð²."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.communications.feedbacks import FeedbacksCollector
from src.repositories.communications.feedbacks import FeedbacksRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class FeedbacksSyncService(BaseService):

    async def sync_feedbacks(self, session: AsyncSession) -> dict:
        """
        ÐŸÐ¾Ð»Ð½Ð°Ñ Ð²Ñ‹Ð³Ñ€ÑƒÐ·ÐºÐ° Ð²ÑÐµÑ… Ð¾Ñ‚Ð·Ñ‹Ð²Ð¾Ð² (Ð¾Ñ‚Ð²ÐµÑ‡ÐµÐ½Ð½Ñ‹Ñ… Ð¸ Ð½ÐµÐ¾Ñ‚Ð²ÐµÑ‡ÐµÐ½Ð½Ñ‹Ñ…).
        Ð˜ÑÐ¿Ð¾Ð»ÑŒÐ·ÑƒÐµÑ‚ offset-based Ð¿Ð°Ð³Ð¸Ð½Ð°Ñ†Ð¸ÑŽ Ð¿Ð¾ Ð¾Ð±Ð¾Ð¸Ð¼ ÑÑ‚Ð°Ñ‚ÑƒÑÐ°Ð¼.
        """
        repo = FeedbacksRepository(session)
        all_feedbacks: list[dict] = []

        async with FeedbacksCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                limit = 50  # WB Ñ‚Ð°Ð¹Ð¼Ð°ÑƒÑ‚Ð¸Ñ‚ Ð¿Ñ€Ð¸ Ð±Ð¾Ð»ÑŒÑˆÐ¸Ñ… Ð±Ð°Ñ‚Ñ‡Ð°Ñ…
                while True:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=limit,
                        offset=offset,
                        order="dateDesc",
                    )
                    feedbacks = (response.data or {}).get("feedbacks", [])
                    if not feedbacks:
                        break
                    all_feedbacks.extend(feedbacks)
                    logger.info(f"Feedbacks: is_answered={is_answered}, offset={offset}, batch={len(feedbacks)}")
                    offset += limit

        saved = await repo.upsert_many(all_feedbacks)
        logger.info(f"Feedbacks synced: {saved} records saved")
        return {"synced": saved, "source": "full"}

    async def sync_feedbacks_incremental(self, session: AsyncSession) -> dict:
        """
        Ð˜Ð½ÐºÑ€ÐµÐ¼ÐµÐ½Ñ‚Ð°Ð»ÑŒÐ½Ð°Ñ Ð²Ñ‹Ð³Ñ€ÑƒÐ·ÐºÐ° Ð¾Ñ‚Ð·Ñ‹Ð²Ð¾Ð² â€” Ð·Ð°Ð³Ñ€ÑƒÐ¶Ð°ÐµÑ‚ Ñ‚Ð¾Ð»ÑŒÐºÐ¾ Ð½Ð¾Ð²Ñ‹Ðµ, Ð½Ð°Ñ‡Ð¸Ð½Ð°Ñ Ñ max(created_date).
        Ð•ÑÐ»Ð¸ Ð‘Ð” Ð¿ÑƒÑÑ‚Ð° â€” fallback Ð½Ð° Ð¿Ð¾Ð»Ð½ÑƒÑŽ ÑÐ¸Ð½Ñ…Ñ€Ð¾Ð½Ð¸Ð·Ð°Ñ†Ð¸ÑŽ.
        """
        repo = FeedbacksRepository(session)
        max_date = await repo.get_max_date()

        if max_date is None:
            logger.info("Feedbacks incremental: no data in DB, falling back to full sync")
            result = await self.sync_feedbacks(session)
            result["source"] = "incremental_fallback_full"
            return result

        # WB API Ð¿Ñ€Ð¸Ð½Ð¸Ð¼Ð°ÐµÑ‚ dateFrom ÐºÐ°Ðº unix timestamp (ÑÐµÐºÑƒÐ½Ð´Ñ‹)
        date_from_ts = str(int(max_date.timestamp()))
        all_feedbacks: list[dict] = []

        async with FeedbacksCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                limit = 50
                while True:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=limit,
                        offset=offset,
                        order="dateDesc",
                        date_from=date_from_ts,
                    )
                    feedbacks = (response.data or {}).get("feedbacks", [])
                    if not feedbacks:
                        break
                    all_feedbacks.extend(feedbacks)
                    logger.info(f"Feedbacks incremental: is_answered={is_answered}, offset={offset}, batch={len(feedbacks)}")
                    offset += limit

        saved = await repo.upsert_many(all_feedbacks)
        logger.info(f"Feedbacks incremental synced: {saved} records (from_date={max_date.isoformat()})")
        return {"synced": saved, "source": "incremental", "from_date": max_date.isoformat()}

