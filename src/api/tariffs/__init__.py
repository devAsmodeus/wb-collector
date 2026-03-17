"""Router: Тарифы WB (10) — 5 endpoints."""
from litestar import Router
from src.api.tariffs.tariffs import TariffsController

tariffs_router = Router(path="/tariffs", route_handlers=[TariffsController])
