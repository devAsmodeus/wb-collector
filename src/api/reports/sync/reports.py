"""Sync: Reports — Синхронизация отчётов WB в БД."""
from datetime import datetime, timedelta

from litestar import Controller, post
from litestar.params import Parameter
from src.services.reports.sync.reports import ReportsSyncService
from src.utils.db_manager import DBManager


def _default_date_from() -> str:
    """Дата год назад в формате RFC3339 (YYYY-MM-DD)."""
    return (datetime.utcnow() - timedelta(days=365)).strftime("%Y-%m-%d")


class SyncStocksController(Controller):
    path = "/stocks"
    tags = ["12. Синхронизация"]

    @post(
        "/",
        summary="Синхронизация остатков на складах",
        description=(
            "Загружает остатки товаров на складах WB и сохраняет в `wb_stocks`.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/stocks`\n\n"
            "По умолчанию — за последний год."
        ),
    )
    async def sync_stocks(
        self,
        date_from: str | None = Parameter(
            default=None, query="dateFrom",
            description="Дата обновления (YYYY-MM-DDTHH:MM:SS). По умолчанию — год назад.",
        ),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_stocks(db.session, date_from or _default_date_from())


    @post(
        "/incremental",
        summary="Инкрементальная синхронизация остатков",
        description=(
            "Загружает только новые остатки (начиная с последней `lastChangeDate` в БД).\n\n"
            "Если БД пуста — автоматически делает полную выгрузку за год.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/stocks`"
        ),
    )
    async def sync_stocks_incremental(self) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_stocks_incremental(db.session)


class SyncOrdersController(Controller):
    path = "/orders"
    tags = ["12. Синхронизация"]

    @post(
        "/",
        summary="Синхронизация заказов",
        description=(
            "Загружает заказы за период и сохраняет в `wb_orders_report`.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/orders`\n\n"
            "По умолчанию — за последний год."
        ),
    )
    async def sync_orders(
        self,
        date_from: str | None = Parameter(
            default=None, query="dateFrom",
            description="Дата начала (YYYY-MM-DDTHH:MM:SS). По умолчанию — год назад.",
        ),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_orders(db.session, date_from or _default_date_from())


    @post(
        "/incremental",
        summary="Инкрементальная синхронизация заказов",
        description=(
            "Загружает только новые заказы (начиная с последней `lastChangeDate` в БД).\n\n"
            "Если БД пуста — автоматически делает полную выгрузку за год.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/orders`"
        ),
    )
    async def sync_orders_incremental(self) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_orders_incremental(db.session)


class SyncSalesController(Controller):
    path = "/sales"
    tags = ["12. Синхронизация"]

    @post(
        "/",
        summary="Синхронизация продаж и возвратов",
        description=(
            "Загружает продажи и возвраты за период и сохраняет в `wb_sales_report`.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/sales`\n\n"
            "По умолчанию — за последний год."
        ),
    )
    async def sync_sales(
        self,
        date_from: str | None = Parameter(
            default=None, query="dateFrom",
            description="Дата начала (YYYY-MM-DDTHH:MM:SS). По умолчанию — год назад.",
        ),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_sales(db.session, date_from or _default_date_from())

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация продаж",
        description=(
            "Загружает только новые продажи/возвраты (начиная с последней `lastChangeDate` в БД).\n\n"
            "Если БД пуста — автоматически делает полную выгрузку за год.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/sales`"
        ),
    )
    async def sync_sales_incremental(self) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_sales_incremental(db.session)
