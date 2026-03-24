"""DB: Finances (13) — Финансы."""
from litestar import Router
from src.api.finances.db.finances import DbFinancialReportController

finances_db_router = Router(
    path="/db",
    route_handlers=[DbFinancialReportController],
)
