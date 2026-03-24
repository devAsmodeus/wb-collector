"""Router: Самовывоз (06) — Click & Collect."""
from litestar import Router

from src.api.pickup.wb import pickup_wb_router
from src.api.pickup.sync import pickup_sync_router
from src.api.pickup.db import pickup_db_router

pickup_router = Router(
    path="/pickup",
    route_handlers=[pickup_wb_router, pickup_sync_router, pickup_db_router],
)
