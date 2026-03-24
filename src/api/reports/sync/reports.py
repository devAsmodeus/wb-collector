"""Sync: Reports — Синхронизация отчётов WB в БД."""
from litestar import Controller, post
from litestar.params import Parameter
from src.services.reports.sync.reports import ReportsSyncService
from src.utils.db_manager import DBManager


class SyncStocksController(Controller):
    path = "/stocks"
    tags = ["Sync / Reports"]

    @post(
        "/",
        summary="Синхронизация остатков на складах",
        description=(
            "Загружает остатки товаров на складах WB и сохраняет в `wb_stocks`.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/stocks`"
        ),
    )
    async def sync_stocks(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата обновления в формате `YYYY-MM-DDTHH:MM:SS`."),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_stocks(db.session, date_from)


class SyncOrdersController(Controller):
    path = "/orders"
    tags = ["Sync / Reports"]

    @post(
        "/",
        summary="Синхронизация заказов",
        description=(
            "Загружает заказы за период и сохраняет в `wb_orders_report`.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/orders`"
        ),
    )
    async def sync_orders(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DDTHH:MM:SS`."),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_orders(db.session, date_from)


class SyncSalesController(Controller):
    path = "/sales"
    tags = ["Sync / Reports"]

    @post(
        "/",
        summary="Синхронизация продаж и возвратов",
        description=(
            "Загружает продажи и возвраты за период и сохраняет в `wb_sales_report`.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/sales`"
        ),
    )
    async def sync_sales(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DDTHH:MM:SS`."),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsSyncService().sync_sales(db.session, date_from)
