"""Router: General (01) — Общее."""
from litestar import Router
from src.api.general.wb import general_wb_router
from src.api.general.sync import general_sync_router
from src.api.general.db import general_db_router

general_router = Router(
    path="/general",
    route_handlers=[general_wb_router, general_sync_router, general_db_router],
)
