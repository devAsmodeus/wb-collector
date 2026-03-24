"""Sync: Reports (12) — Отчёты."""
from litestar import Router
from src.api.reports.sync.reports import SyncStocksController, SyncOrdersController, SyncSalesController

reports_sync_router = Router(
    path="/sync",
    route_handlers=[SyncStocksController, SyncOrdersController, SyncSalesController],
)
