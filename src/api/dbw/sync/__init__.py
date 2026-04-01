"""Sync: DBW (04)."""
from litestar import Router
from src.api.dbw.sync.orders import SyncDBWOrdersController

dbw_sync_router = Router(
    path="/sync",
    route_handlers=[SyncDBWOrdersController],
)
