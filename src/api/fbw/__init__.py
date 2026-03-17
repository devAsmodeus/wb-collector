"""Router: FBW (07) — Поставки FBW (7 endpoints)."""
from litestar import Router

from src.api.fbw.acceptance import FBWAcceptanceController
from src.api.fbw.supplies import FBWSuppliesController

fbw_router = Router(
    path="/fbw",
    route_handlers=[FBWAcceptanceController, FBWSuppliesController],
)
