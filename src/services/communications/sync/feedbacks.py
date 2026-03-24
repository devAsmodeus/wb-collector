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
                limit = 100
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
                    offset += limit

        saved = await repo.upsert_many(all_feedbacks)
        logger.info(f"Feedbacks synced: {saved} records saved")
        return {"synced": saved, "source": "full"}
