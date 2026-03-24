"""Sync: DBS (05)."""
from litestar import Router
from src.api.dbs.sync.orders import SyncDBSOrdersController

dbs_sync_router = Router(
    path="/sync",
    route_handlers=[SyncDBSOrdersController],
)
