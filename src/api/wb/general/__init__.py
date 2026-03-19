"""WB API proxy: General (01)."""
from litestar import Router
from src.api.wb.general.ping import WbPingController
from src.api.wb.general.seller import WbSellerController
from src.api.wb.general.news import WbNewsController

wb_general_router = Router(
    path="/general",
    route_handlers=[WbPingController, WbSellerController, WbNewsController],
)
