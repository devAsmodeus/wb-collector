"""WB API proxy: Finances (13) — Финансы."""
from litestar import Router
from src.api.finances.wb.finances import FinancesWbController

finances_wb_router = Router(
    path="/wb",
    route_handlers=[FinancesWbController],
)
