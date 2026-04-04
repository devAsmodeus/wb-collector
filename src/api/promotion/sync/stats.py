"""Sync: Маркетинг / Статистика кампаний."""
from litestar import Controller, post
from src.tasks.celery_app import celery_app


class SyncStatsController(Controller):
    path = "/stats"
    tags = ["08. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка статистики кампаний в БД (Celery)",
        description=(
            "Запускает Celery-задачу для загрузки статистики по всем кампаниям.\n\n"
            "Задача выполняется в фоне (1118+ кампаний, ~8 минут из-за rate-limit WB).\n\n"
            "**WB:** `GET advert-api.wildberries.ru/adv/v3/fullstats`"
        ),
        status_code=202,
    )
    async def sync_stats_full(self) -> dict:
        task = celery_app.send_task("sync.promotion.stats_full")
        return {"task_id": task.id, "status": "queued", "source": "full"}

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка статистики кампаний в БД (Celery)",
        description=(
            "Запускает Celery-задачу для обновления статистики кампаний.\n\n"
            "**WB:** `GET advert-api.wildberries.ru/adv/v3/fullstats`"
        ),
        status_code=202,
    )
    async def sync_stats_incremental(self) -> dict:
        task = celery_app.send_task("sync.promotion.stats_full")
        return {"task_id": task.id, "status": "queued", "source": "incremental"}
