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
                while True:
                    response = await collector.get_list(
                        is_answered=is_answered,
                        limit=limit,
                        offset=offset,
                        order="dateDesc",
                    )
                    questions = response.get("data", {}).get("questions", [])
                    if not questions:
                        break
                    all_questions.extend(questions)
                    offset += limit

        saved = await repo.upsert_many(all_questions)
        logger.info(f"Questions synced: {saved} records saved")
        return {"synced": saved, "source": "full"}
