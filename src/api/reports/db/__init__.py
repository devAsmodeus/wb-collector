"""DB: Reports (12) — Отчёты."""
from litestar import Router
from src.api.reports.db.reports import DbStocksController, DbOrdersController, DbSalesController

reports_db_router = Router(
    path="/db",
    route_handlers=[DbStocksController, DbOrdersController, DbSalesController],
)
