"""Router: FBS (03) — Заказы FBS (34 endpoints)."""
from litestar import Router

from src.api.fbs.wb import fbs_wb_router
from src.api.fbs.sync import fbs_sync_router
from src.api.fbs.db import fbs_db_router

fbs_router = Router(
    path="/fbs",
    route_handlers=[fbs_wb_router, fbs_sync_router, fbs_db_router],
)
