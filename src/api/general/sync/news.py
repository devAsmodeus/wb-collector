"""Sync: General / Новости."""
from http import HTTPStatus
from litestar import Controller, post
from src.services.general.sync.news import NewsSyncService
from src.utils.db_manager import DBManager


class SyncNewsController(Controller):
    path = "/news"
    tags = ["01. Синхронизация"]

    @post(
        "/full",
        status_code=HTTPStatus.ACCEPTED,
        summary="Полная выгрузка новостей в БД (Celery)",
        description=(
            "Запускает выгрузку всех новостей через Celery (WB rate limit: 1 req/min — может занять несколько минут).\n\n"
            "Возвращает `task_id`. Данные в БД появятся по окончании задачи.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/communications/v2/news`"
        ),
    )
    async def sync_news_full(self) -> dict:
        from src.tasks.tasks import sync_general_news_full
        task = sync_general_news_full.delay()
        return {"task_id": task.id, "status": "queued"}

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация новостей",
        description=(
            "Загружает только новые новости (начиная с последнего `news_id` в БД).\n\n"
            "Если БД пуста — автоматически делает полную выгрузку.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/communications/v2/news`"
        ),
    )
    async def sync_news_incremental(self) -> dict:
        async with DBManager() as db:
            return await NewsSyncService().sync_incremental(db.session)
