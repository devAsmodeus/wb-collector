"""Ð¡ÐµÑ€Ð²Ð¸Ñ Sync: ÐšÐ¾Ð¼Ð¼ÑƒÐ½Ð¸ÐºÐ°Ñ†Ð¸Ð¸ â€” Ð¡Ð¸Ð½Ñ…Ñ€Ð¾Ð½Ð¸Ð·Ð°Ñ†Ð¸Ñ Ð²Ð¾Ð¿Ñ€Ð¾ÑÐ¾Ð²."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.communications.questions import QuestionsCollector
from src.exceptions import WBApiException
from src.repositories.communications.questions import QuestionsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class QuestionsSyncService(BaseService):

    async def sync_questions(self, session: AsyncSession) -> dict:
        """
        ÐŸÐ¾Ð»Ð½Ð°Ñ Ð²Ñ‹Ð³Ñ€ÑƒÐ·ÐºÐ° Ð²ÑÐµÑ… Ð²Ð¾Ð¿Ñ€Ð¾ÑÐ¾Ð² (Ð¾Ñ‚Ð²ÐµÑ‡ÐµÐ½Ð½Ñ‹Ñ… Ð¸ Ð½ÐµÐ¾Ñ‚Ð²ÐµÑ‡ÐµÐ½Ð½Ñ‹Ñ…).
        Ð˜ÑÐ¿Ð¾Ð»ÑŒÐ·ÑƒÐµÑ‚ offset-based Ð¿Ð°Ð³Ð¸Ð½Ð°Ñ†Ð¸ÑŽ Ð¿Ð¾ Ð¾Ð±Ð¾Ð¸Ð¼ ÑÑ‚Ð°Ñ‚ÑƒÑÐ°Ð¼.
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
                    try:
                        response = await collector.get_list(
                            is_answered=is_answered,
                            limit=min(limit, max_skip - offset),
                            offset=offset,
                            order="dateDesc",
                        )
                    except WBApiException as e:
                        if e.status_code == 422:
                            logger.info(f"Questions: WB limit at offset={offset}, stopping")
                        else:
                            logger.error(f"Questions: WB error {e.status_code} at offset={offset}")
                        break
                    questions = (response.data or {}).get("questions", [])
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
        Ð˜Ð½ÐºÑ€ÐµÐ¼ÐµÐ½Ñ‚Ð°Ð»ÑŒÐ½Ð°Ñ Ð²Ñ‹Ð³Ñ€ÑƒÐ·ÐºÐ° Ð²Ð¾Ð¿Ñ€Ð¾ÑÐ¾Ð² â€” Ð·Ð°Ð³Ñ€ÑƒÐ¶Ð°ÐµÑ‚ Ñ‚Ð¾Ð»ÑŒÐºÐ¾ Ð½Ð¾Ð²Ñ‹Ðµ, Ð½Ð°Ñ‡Ð¸Ð½Ð°Ñ Ñ max(created_date).
        Ð•ÑÐ»Ð¸ Ð‘Ð” Ð¿ÑƒÑÑ‚Ð° â€” fallback Ð½Ð° Ð¿Ð¾Ð»Ð½ÑƒÑŽ ÑÐ¸Ð½Ñ…Ñ€Ð¾Ð½Ð¸Ð·Ð°Ñ†Ð¸ÑŽ.
        """
        repo = QuestionsRepository(session)
        max_date = await repo.get_max_date()

        if max_date is None:
            logger.info("Questions incremental: no data in DB, falling back to full sync")
            result = await self.sync_questions(session)
            result["source"] = "incremental_fallback_full"
            return result

        # WB API Ð¿Ñ€Ð¸Ð½Ð¸Ð¼Ð°ÐµÑ‚ dateFrom ÐºÐ°Ðº unix timestamp (ÑÐµÐºÑƒÐ½Ð´Ñ‹)
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
                    questions = (response.data or {}).get("questions", [])
                    if not questions:
                        break
                    all_questions.extend(questions)
                    logger.info(f"Questions incremental: is_answered={is_answered}, offset={offset}, batch={len(questions)}")
                    offset += limit

        saved = await repo.upsert_many(all_questions)
        logger.info(f"Questions incremental synced: {saved} records (from_date={max_date.isoformat()})")
        return {"synced": saved, "source": "incremental", "from_date": max_date.isoformat()}

