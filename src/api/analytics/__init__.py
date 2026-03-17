"""Router: Аналитика WB (11) — 16 endpoints."""
from litestar import Router
from src.api.analytics.analytics import AnalyticsController

analytics_router = Router(path="/analytics", route_handlers=[AnalyticsController])
