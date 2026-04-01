"""WB API proxy: Маркетинг (08) — Продвижение."""
from litestar import Router

from src.api.promotion.wb.campaigns import CampaignsController
from src.api.promotion.wb.finance import FinanceController
from src.api.promotion.wb.search import SearchController
from src.api.promotion.wb.stats import StatsController
from src.api.promotion.wb.calendar import CalendarController

promotion_wb_router = Router(
    path="/wb",
    route_handlers=[
        CampaignsController,
        FinanceController,
        SearchController,
        StatsController,
        CalendarController,
    ],
)
