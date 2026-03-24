"""Router: DBS (05) — Заказы DBS."""
from litestar import Router

from src.api.dbs.wb import dbs_wb_router
from src.api.dbs.sync import dbs_sync_router
from src.api.dbs.db import dbs_db_router

dbs_router = Router(
    path="/dbs",
    route_handlers=[dbs_wb_router, dbs_sync_router, dbs_db_router],
)
