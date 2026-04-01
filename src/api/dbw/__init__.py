"""Router: DBW (04) — Заказы DBW."""
from litestar import Router

from src.api.dbw.wb import dbw_wb_router
from src.api.dbw.sync import dbw_sync_router
from src.api.dbw.db import dbw_db_router

dbw_router = Router(
    path="/dbw",
    route_handlers=[dbw_wb_router, dbw_sync_router, dbw_db_router],
)
