"""Sync: Маркетинг (08) — Продвижение."""
from litestar import Router

from src.api.promotion.sync.campaigns import SyncCampaignsController
from src.api.promotion.sync.stats import SyncStatsController
from src.api.promotion.sync.calendar import SyncCalendarController

promotion_sync_router = Router(
    path="/sync",
    route_handlers=[
        SyncCampaignsController,
        SyncStatsController,
        SyncCalendarController,
    ],
)
