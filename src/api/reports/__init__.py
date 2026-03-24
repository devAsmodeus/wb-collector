"""Router: Reports (12) — Отчёты."""
from litestar import Router

from src.api.reports.wb import reports_wb_router
from src.api.reports.sync import reports_sync_router
from src.api.reports.db import reports_db_router

reports_router = Router(
    path="/reports",
    route_handlers=[reports_wb_router, reports_sync_router, reports_db_router],
)
