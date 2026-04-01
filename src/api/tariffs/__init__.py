"""Router: Tariffs (10) — Тарифы."""
from litestar import Router

from src.api.tariffs.wb import tariffs_wb_router
from src.api.tariffs.sync import tariffs_sync_router
from src.api.tariffs.db import tariffs_db_router

tariffs_router = Router(
    path="/tariffs",
    route_handlers=[tariffs_wb_router, tariffs_sync_router, tariffs_db_router],
)
