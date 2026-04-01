"""Router: Finances (13) — Финансы."""
from litestar import Router

from src.api.finances.wb import finances_wb_router
from src.api.finances.sync import finances_sync_router
from src.api.finances.db import finances_db_router

finances_router = Router(
    path="/finances",
    route_handlers=[finances_wb_router, finances_sync_router, finances_db_router],
)
