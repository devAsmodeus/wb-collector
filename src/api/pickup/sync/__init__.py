"""Sync: Самовывоз (06)."""
from litestar import Router
from src.api.pickup.sync.orders import SyncPickupOrdersController

pickup_sync_router = Router(
    path="/sync",
    route_handlers=[SyncPickupOrdersController],
)
