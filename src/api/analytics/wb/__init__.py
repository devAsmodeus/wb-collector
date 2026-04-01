"""WB API proxy: Analytics (11) — Аналитика."""
from litestar import Router
from src.api.analytics.wb.analytics import AnalyticsWbController

analytics_wb_router = Router(
    path="/wb",
    route_handlers=[AnalyticsWbController],
)
