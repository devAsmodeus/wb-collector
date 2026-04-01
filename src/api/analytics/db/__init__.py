"""DB: Analytics (11) — Аналитика."""
from litestar import Router

from src.api.analytics.db.funnel import DbFunnelController
from src.api.analytics.db.search import DbSearchController
from src.api.analytics.db.stocks import DbStocksController

analytics_db_router = Router(
    path="/db",
    route_handlers=[DbFunnelController, DbSearchController, DbStocksController],
)
