"""Sync: FBW (07) — Поставки FBW."""
from litestar import Router

fbw_sync_router = Router(
    path="/sync",
    route_handlers=[],
)
