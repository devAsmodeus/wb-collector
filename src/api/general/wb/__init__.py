"""WB API proxy: General (01)."""
from litestar import Router
from src.api.general.wb.ping import WbPingController
from src.api.general.wb.seller import WbSellerController
from src.api.general.wb.news import WbNewsController

general_wb_router = Router(
    path="/wb",
    route_handlers=[WbPingController, WbSellerController, WbNewsController],
)
