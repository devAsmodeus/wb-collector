"""Sync: General (01)."""
from litestar import Router
from src.api.sync.general.seller import SyncSellerController
from src.api.sync.general.news import SyncNewsController

sync_general_router = Router(
    path="/general",
    route_handlers=[SyncSellerController, SyncNewsController],
)
