"""Сервис Sync: Коммуникации — Синхронизация отзывов."""
import logging
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.communications.feedbacks import FeedbacksCollector
from src.repositories.communications.feedbacks import FeedbacksRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)

# Максимум страниц за один sync (защита от бесконечного цикла)
MAX_PAGES_PER_SYNC = 20
BATCH_SIZE = 50


class FeedbacksSyncService(BaseService):

    async def sync_feedbacks_historical(self, session: AsyncSession) -> dict:
        """
        Полный исторический дамп всех отзывов без лимита страниц.
        Предназначен для первоначальной загрузки через Celery (может занять часы).
        116k+ отзывов — не запускать через HTTP.
        """
        repo = FeedbacksRepository(session)
        total_saved = 0

        async with FeedbacksCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                page = 0
                while True:
                    page += 1
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=BATCH_SIZE,
                        offset=offset,
                        order="dateDesc",
                    )
                    feedbacks = (response.data or {}).get("feedbacks", [])
                    if not feedbacks:
                        break
                    saved = await repo.upsert_many(feedbacks)
                    total_saved += saved
                    logger.info(
                        f"Feedbacks historical: is_answered={is_answered}, "
                        f"page={page}, offset={offset}, batch={len(feedbacks)}, total={total_saved}"
                    )
                    if len(feedbacks) < BATCH_SIZE:
                        break
                    offset += BATCH_SIZE

        logger.info(f"Feedbacks historical sync done: {total_saved} total")
        return {"synced": total_saved, "source": "historical"}

    # Алиас для обратной совместимости с Celery-задачей
    async def sync_feedbacks_full(self, session: AsyncSession) -> dict:
        return await self.sync_feedbacks(session)

    async def sync_feedbacks(self, session: AsyncSession) -> dict:
        """
        Синхронизация свежих отзывов (последние 30 дней).
        116k+ отзывов за всё время — полный sync слишком долгий.
        Для исторических данных используй sync_feedbacks_all.
        """
        repo = FeedbacksRepository(session)

        # Дата 30 дней назад как unix timestamp
        date_from_ts = str(int((datetime.utcnow() - timedelta(days=30)).timestamp()))

        all_feedbacks: list[dict] = []

        async with FeedbacksCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                pages = 0
                while pages < MAX_PAGES_PER_SYNC:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=BATCH_SIZE,
                        offset=offset,
                        order="dateDesc",
                        date_from=date_from_ts,
                    )
                    feedbacks = (response.data or {}).get("feedbacks", [])
                    if not feedbacks:
                        break
                    all_feedbacks.extend(feedbacks)
                    logger.info(
                        f"Feedbacks: is_answered={is_answered}, "
                        f"offset={offset}, batch={len(feedbacks)}"
                    )
                    if len(feedbacks) < BATCH_SIZE:
                        break
                    offset += BATCH_SIZE
                    pages += 1

        saved = await repo.upsert_many(all_feedbacks)
        logger.info(f"Feedbacks synced: {saved} records saved")
        return {"synced": saved, "source": "full_30d"}

    async def sync_feedbacks_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация — загружает только новые отзывы
        начиная с max(created_date) из БД. Если БД пуста — fallback на 30 дней.
        """
        repo = FeedbacksRepository(session)
        max_date = await repo.get_max_date()

        if max_date is None:
            logger.info("Feedbacks incremental: no data in DB, falling back to 30-day sync")
            result = await self.sync_feedbacks(session)
            result["source"] = "incremental_fallback_30d"
            return result

        # Берём с небольшим перекрытием (-1 час) чтобы не пропустить
        date_from_ts = str(int((max_date - timedelta(hours=1)).timestamp()))
        all_feedbacks: list[dict] = []

        async with FeedbacksCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                pages = 0
                while pages < MAX_PAGES_PER_SYNC:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=BATCH_SIZE,
                        offset=offset,
                        order="dateDesc",
                        date_from=date_from_ts,
                    )
                    feedbacks = (response.data or {}).get("feedbacks", [])
                    if not feedbacks:
                        break
                    all_feedbacks.extend(feedbacks)
                    logger.info(
                        f"Feedbacks incremental: is_answered={is_answered}, "
                        f"offset={offset}, batch={len(feedbacks)}"
                    )
                    if len(feedbacks) < BATCH_SIZE:
                        break
                    offset += BATCH_SIZE
                    pages += 1

        saved = await repo.upsert_many(all_feedbacks)
        logger.info(
            f"Feedbacks incremental synced: {saved} records "
            f"(from_date={max_date.isoformat()})"
        )
        return {
            "synced": saved,
            "source": "incremental",
            "from_date": max_date.isoformat(),
        }


    async def sync_feedbacks_historical(self, session: AsyncSession) -> dict:
        """
        Разовая полная выгрузка всех 116k+ отзывов.
        Запускается через Celery task (time_limit=6h), не через HTTP.
        Не ограничивает диапазон дат — загружает всё.
        """
        repo = FeedbacksRepository(session)
        total_saved = 0
        CHUNK = 50

        async with FeedbacksCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                page = 0
                while True:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=CHUNK,
                        offset=offset,
                        order="dateDesc",
                    )
                    feedbacks = (response.data or {}).get("feedbacks", [])
                    if not feedbacks:
                        break
                    saved = await repo.upsert_many(feedbacks)
                    total_saved += saved
                    page += 1
                    if page % 100 == 0:
                        logger.info(f"Historical feedbacks: is_answered={is_answered}, page={page}, total={total_saved}")
                    if len(feedbacks) < CHUNK:
                        break
                    offset += CHUNK

        logger.info(f"Historical feedbacks done: {total_saved} total")
        return {"synced": total_saved, "source": "historical"}
