"""Sync: Finances — Синхронизация финансовых отчётов WB в БД."""
from datetime import datetime, timedelta

from litestar import Controller, post
from litestar.params import Parameter
from src.services.finances.sync.finances import FinancesSyncService
from src.tasks.celery_app import celery_app
from src.utils.db_manager import DBManager


class SyncFinancialReportController(Controller):
    path = "/full"
    tags = ["13. Синхронизация"]

    @post(
        "/",
        summary="Полная синхронизация финансового отчёта (Celery)",
        description=(
            "Запускает Celery-задачу для загрузки детального финансового отчёта.\n\n"
            "Задача выполняется в фоне (1M+ строк, может занять несколько минут).\n\n"
            "**WB:** `GET seller-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod`"
        ),
        status_code=202,
    )
    async def sync_financial_report(
        self,
        date_from: str | None = Parameter(
            default=None, query="dateFrom",
            description="Дата начала периода (YYYY-MM-DD). По умолчанию — 30 дней назад.",
        ),
        date_to: str | None = Parameter(
            default=None, query="dateTo",
            description="Дата окончания периода (YYYY-MM-DD). По умолчанию — сегодня.",
        ),
    ) -> dict:
        if not date_from:
            date_from = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not date_to:
            date_to = datetime.utcnow().strftime("%Y-%m-%d")
        task = celery_app.send_task("sync.finances.full", kwargs={"date_from": date_from, "date_to": date_to})
        return {"task_id": task.id, "status": "queued", "date_from": date_from, "date_to": date_to}


class SyncFinancialReportIncrementalController(Controller):
    path = "/incremental"
    tags = ["13. Синхронизация"]

    @post(
        "/",
        summary="Инкрементальная синхронизация финансового отчёта",
        description=(
            "Загружает только новые записи финансового отчёта, начиная с max(rrd_id) из БД.\n\n"
            "Если БД пуста — выполняет полную синхронизацию.\n\n"
            "**WB:** `GET seller-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod`"
        ),
    )
    async def sync_financial_report_incremental(
        self,
        date_from: str | None = Parameter(
            default=None, query="dateFrom",
            description="Дата начала периода (YYYY-MM-DD). По умолчанию — 90 дней назад.",
        ),
        date_to: str | None = Parameter(
            default=None, query="dateTo",
            description="Дата окончания периода (YYYY-MM-DD). По умолчанию — сегодня.",
        ),
    ) -> dict:
        if not date_from:
            date_from = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
        if not date_to:
            date_to = datetime.utcnow().strftime("%Y-%m-%d")
        async with DBManager() as db:
            return await FinancesSyncService().sync_financial_report_incremental(db.session, date_from, date_to)
