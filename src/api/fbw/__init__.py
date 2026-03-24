"""Router: FBW (07) — Поставки FBW."""
from litestar import Router

from src.api.fbw.wb import fbw_wb_router
from src.api.fbw.sync import fbw_sync_router
from src.api.fbw.db import fbw_db_router

fbw_router = Router(
    path="/fbw",
    route_handlers=[fbw_wb_router, fbw_sync_router, fbw_db_router],
)
