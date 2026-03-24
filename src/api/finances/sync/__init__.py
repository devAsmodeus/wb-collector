"""Sync: Finances (13) — Финансы."""
from litestar import Router
from src.api.finances.sync.finances import SyncFinancialReportController

finances_sync_router = Router(
    path="/sync",
    route_handlers=[SyncFinancialReportController],
)
