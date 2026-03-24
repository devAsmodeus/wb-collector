"""Router: Communications (09) — Вопросы, отзывы, чат."""
from litestar import Router

from src.api.communications.wb import communications_wb_router
from src.api.communications.sync import communications_sync_router
from src.api.communications.db import communications_db_router

communications_router = Router(
    path="/communications",
    route_handlers=[communications_wb_router, communications_sync_router, communications_db_router],
)
