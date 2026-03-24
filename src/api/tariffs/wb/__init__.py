"""WB API proxy: Tariffs (10) — Тарифы."""
from litestar import Router
from src.api.tariffs.wb.tariffs import TariffsWbController

tariffs_wb_router = Router(
    path="/wb",
    route_handlers=[TariffsWbController],
)
