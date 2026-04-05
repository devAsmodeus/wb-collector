"""Sync: FBS (03)."""
from litestar import Router
from src.api.fbs.sync.orders import SyncFbsOrdersController
from src.api.fbs.sync.supplies import SyncFbsSuppliesController
from src.api.fbs.sync.passes import SyncFbsPassesController

fbs_sync_router = Router(
    path="/sync",
    route_handlers=[SyncFbsOrdersController, SyncFbsSuppliesController, SyncFbsPassesController],
)
