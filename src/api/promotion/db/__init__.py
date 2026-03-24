"""DB: Маркетинг (08) — Продвижение."""
from litestar import Router

from src.api.promotion.db.campaigns import DbCampaignsController
from src.api.promotion.db.stats import DbStatsController
from src.api.promotion.db.calendar import DbCalendarController

promotion_db_router = Router(
    path="/db",
    route_handlers=[
        DbCampaignsController,
        DbStatsController,
        DbCalendarController,
    ],
)
