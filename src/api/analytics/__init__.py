"""Router: Analytics (11) — Аналитика."""
from litestar import Router

from src.api.analytics.wb import analytics_wb_router
from src.api.analytics.sync import analytics_sync_router
from src.api.analytics.db import analytics_db_router

analytics_router = Router(
    path="/analytics",
    route_handlers=[analytics_wb_router, analytics_sync_router, analytics_db_router],
)
