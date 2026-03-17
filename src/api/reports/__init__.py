"""Router: Отчёты WB (12) — 25 endpoints."""
from litestar import Router
from src.api.reports.reports import ReportsController

reports_router = Router(path="/reports", route_handlers=[ReportsController])
