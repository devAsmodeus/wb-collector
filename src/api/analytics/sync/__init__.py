"""Sync: Analytics (11) — Аналитика."""
from litestar import Router

from src.api.analytics.sync.funnel import SyncFunnelController
from src.api.analytics.sync.search import SyncSearchController
from src.api.analytics.sync.stocks import SyncStocksController

analytics_sync_router = Router(
    path="/sync",
    route_handlers=[SyncFunnelController, SyncSearchController, SyncStocksController],
)
