"""Sync: General (01)."""
from litestar import Router
from src.api.general.sync.seller import SyncSellerController
from src.api.general.sync.news import SyncNewsController

general_sync_router = Router(
    path="/sync",
    route_handlers=[SyncSellerController, SyncNewsController],
)
