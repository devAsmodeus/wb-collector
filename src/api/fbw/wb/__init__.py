"""WB API proxy: FBW (07) — Поставки FBW."""
from litestar import Router

from src.api.fbw.wb.acceptance import FBWAcceptanceController
from src.api.fbw.wb.supplies import FBWSuppliesController

fbw_wb_router = Router(
    path="/wb",
    route_handlers=[FBWAcceptanceController, FBWSuppliesController],
)
