"""WB API proxy: Reports (12) — Отчёты."""
from litestar import Router
from src.api.reports.wb.reports import ReportsWbController

reports_wb_router = Router(
    path="/wb",
    route_handlers=[ReportsWbController],
)
