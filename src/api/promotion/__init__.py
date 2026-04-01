"""Router: Маркетинг (08) — Продвижение (37 endpoints)."""
from litestar import Router

from src.api.promotion.wb import promotion_wb_router
from src.api.promotion.sync import promotion_sync_router
from src.api.promotion.db import promotion_db_router

promotion_router = Router(
    path="/promotion",
    route_handlers=[promotion_wb_router, promotion_sync_router, promotion_db_router],
)
