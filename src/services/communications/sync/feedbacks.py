"""Сервис Sync: Коммуникации — Синхронизация отзывов."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.communications.feedbacks import FeedbacksCollector
from src.repositories.communications.feedbacks import FeedbacksRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class FeedbacksSyncService(BaseService):

    async def sync_feedbacks(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех отзывов (отвеченных и неотвеченных).
        Использует offset-based пагинацию по обоим статусам.
        """
        repo = FeedbacksRepository(session)
        all_feedbacks: list[dict] = []

        async with FeedbacksCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                limit = 50  # WB таймаутит при больших батчах
                while True:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=limit,
                        offset=offset,
                        order="dateDesc",
                    )
                    feedbacks = response.get("data", {}).get("feedbacks", [])
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
        Инкрементальная выгрузка отзывов — загружает только новые, начиная с max(created_date).
        Если БД пуста — fallback на полную синхронизацию.
        """
        repo = FeedbacksRepository(session)
        max_date = await repo.get_max_date()

        if max_date is None:
            logger.info("Feedbacks incremental: no data in DB, falling back to full sync")
            result = await self.sync_feedbacks(session)
            result["source"] = "incremental_fallback_full"
            return result

        # WB API принимает dateFrom как unix timestamp (секунды)
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
                    feedbacks = response.get("data", {}).get("feedbacks", [])
                    if not feedbacks:
                        break
                    all_feedbacks.extend(feedbacks)
                    logger.info(f"Feedbacks incremental: is_answered={is_answered}, offset={offset}, batch={len(feedbacks)}")
                    offset += limit

        saved = await repo.upsert_many(all_feedbacks)
        logger.info(f"Feedbacks incremental synced: {saved} records (from_date={max_date.isoformat()})")
        return {"synced": saved, "source": "incremental", "from_date": max_date.isoformat()}
