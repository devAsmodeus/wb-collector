"""Sync: Communications / Вопросы."""
from litestar import Controller, post
from src.services.communications.sync.questions import QuestionsSyncService
from src.utils.db_manager import DBManager


class SyncQuestionsController(Controller):
    path = "/questions"
    tags = ["09. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка вопросов в БД",
        description=(
            "Загружает все вопросы (отвеченные и неотвеченные) с пагинацией и сохраняет в `wb_questions`.\n\n"
            "**WB:** `GET feedbacks-api.wildberries.ru/api/v1/questions`"
        ),
    )
    async def sync_questions_full(self) -> dict:
        async with DBManager() as db:
            return await QuestionsSyncService().sync_questions(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка вопросов в БД",
        description=(
            "Загружает только новые вопросы, начиная с max(created_date) из БД.\n\n"
            "Если БД пуста — выполняет полную синхронизацию.\n\n"
            "**WB:** `GET feedbacks-api.wildberries.ru/api/v1/questions`"
        ),
    )
    async def sync_questions_incremental(self) -> dict:
        async with DBManager() as db:
            return await QuestionsSyncService().sync_questions_incremental(db.session)
