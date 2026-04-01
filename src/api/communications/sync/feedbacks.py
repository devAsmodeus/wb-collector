"""Sync: Communications / Отзывы."""
from litestar import Controller, post
from src.services.communications.sync.feedbacks import FeedbacksSyncService
from src.utils.db_manager import DBManager


class SyncFeedbacksController(Controller):
    path = "/feedbacks"
    tags = ["09. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка отзывов в БД",
        description=(
            "Загружает все отзывы (отвеченные и неотвеченные) с пагинацией и сохраняет в `wb_feedbacks`.\n\n"
            "**WB:** `GET feedbacks-api.wildberries.ru/api/v1/feedbacks`"
        ),
    )
    async def sync_feedbacks_full(self) -> dict:
        async with DBManager() as db:
            return await FeedbacksSyncService().sync_feedbacks(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка отзывов в БД",
        description=(
            "Загружает только новые отзывы, начиная с max(created_date) из БД.\n\n"
            "Если БД пуста — выполняет полную синхронизацию.\n\n"
            "**WB:** `GET feedbacks-api.wildberries.ru/api/v1/feedbacks`"
        ),
    )
    async def sync_feedbacks_incremental(self) -> dict:
        async with DBManager() as db:
            return await FeedbacksSyncService().sync_feedbacks_incremental(db.session)
