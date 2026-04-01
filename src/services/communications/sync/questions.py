"""Сервис Sync: Коммуникации — Синхронизация вопросов."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.communications.questions import QuestionsCollector
from src.repositories.communications.questions import QuestionsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class QuestionsSyncService(BaseService):

    async def sync_questions(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех вопросов (отвеченных и неотвеченных).
        Использует offset-based пагинацию по обоим статусам.
        """
        repo = QuestionsRepository(session)
        all_questions: list[dict] = []

        async with QuestionsCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                limit = 100
                # WB API: take + skip <= 10000
                max_skip = 10000
                while offset < max_skip:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=min(limit, max_skip - offset),
                        offset=offset,
                        order="dateDesc",
                    )
                    questions = response.get("data", {}).get("questions", [])
                    if not questions:
                        break
                    all_questions.extend(questions)
                    logger.info(f"Questions: is_answered={is_answered}, offset={offset}, batch={len(questions)}")
                    offset += limit

        saved = await repo.upsert_many(all_questions)
        logger.info(f"Questions synced: {saved} records saved")
        return {"synced": saved, "source": "full"}

    async def sync_questions_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная выгрузка вопросов — загружает только новые, начиная с max(created_date).
        Если БД пуста — fallback на полную синхронизацию.
        """
        repo = QuestionsRepository(session)
        max_date = await repo.get_max_date()

        if max_date is None:
            logger.info("Questions incremental: no data in DB, falling back to full sync")
            result = await self.sync_questions(session)
            result["source"] = "incremental_fallback_full"
            return result

        # WB API принимает dateFrom как unix timestamp (секунды)
        date_from_ts = str(int(max_date.timestamp()))
        all_questions: list[dict] = []

        async with QuestionsCollector() as collector:
            for is_answered in [False, True]:
                offset = 0
                limit = 100
                max_skip = 10000
                while offset < max_skip:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=min(limit, max_skip - offset),
                        offset=offset,
                        order="dateDesc",
                        date_from=date_from_ts,
                    )
                    questions = response.get("data", {}).get("questions", [])
                    if not questions:
                        break
                    all_questions.extend(questions)
                    logger.info(f"Questions incremental: is_answered={is_answered}, offset={offset}, batch={len(questions)}")
                    offset += limit

        saved = await repo.upsert_many(all_questions)
        logger.info(f"Questions incremental synced: {saved} records (from_date={max_date.isoformat()})")
        return {"synced": saved, "source": "incremental", "from_date": max_date.isoformat()}
