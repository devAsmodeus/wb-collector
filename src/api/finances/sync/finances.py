"""Sync: Finances — Синхронизация финансовых отчётов WB в БД."""
from litestar import Controller, post
from litestar.params import Parameter
from src.services.finances.sync.finances import FinancesSyncService
from src.utils.db_manager import DBManager


class SyncFinancialReportController(Controller):
    path = "/full"
    tags = ["Sync / Finances"]

    @post(
        "/",
        summary="Полная синхронизация финансового отчёта",
        description=(
            "Загружает детальный финансовый отчёт за период с пагинацией и сохраняет в `wb_financial_report`.\n\n"
            "**WB:** `GET seller-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod`"
        ),
    )
    async def sync_financial_report(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала периода в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="dateTo", description="Дата окончания периода в формате `YYYY-MM-DD`."),
    ) -> dict:
        async with DBManager() as db:
            return await FinancesSyncService().sync_financial_report(db.session, date_from, date_to)
