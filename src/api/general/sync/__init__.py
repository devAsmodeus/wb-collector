"""Sync: General (01)."""
from litestar import Router
from src.api.general.sync.seller import SyncSellerController
from src.api.general.sync.news import SyncNewsController
from src.api.general.sync.rating import SyncRatingController
from src.api.general.sync.subscriptions import SyncSubscriptionsController

general_sync_router = Router(
    path="/sync",
    route_handlers=[SyncSellerController, SyncNewsController, SyncRatingController, SyncSubscriptionsController],
)
