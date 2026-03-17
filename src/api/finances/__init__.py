"""Router: Финансы WB (13) — 6 endpoints."""
from litestar import Router
from src.api.finances.finances import FinancesController

finances_router = Router(path="/finances", route_handlers=[FinancesController])
