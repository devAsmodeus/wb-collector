"""Sync: FBS (03)."""
from litestar import Router
from src.api.fbs.sync.orders import SyncFbsOrdersController

fbs_sync_router = Router(
    path="/sync",
    route_handlers=[SyncFbsOrdersController],
)
