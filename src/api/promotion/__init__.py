"""Router: Маркетинг (08) — Продвижение (37 endpoints)."""
from litestar import Router

from src.api.promotion.campaigns import CampaignsController
from src.api.promotion.finance import FinanceController
from src.api.promotion.search import SearchController
from src.api.promotion.stats import StatsController
from src.api.promotion.calendar import CalendarController

promotion_router = Router(
    path="/promotion",
    route_handlers=[
        CampaignsController,
        FinanceController,
        SearchController,
        StatsController,
        CalendarController,
    ],
)
