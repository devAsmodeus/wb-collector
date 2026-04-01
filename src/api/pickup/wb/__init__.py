"""WB API proxy: Самовывоз (06) — Click & Collect."""
from litestar import Router

from src.api.pickup.wb.orders import PickupOrdersController
from src.api.pickup.wb.meta import PickupMetaController

pickup_wb_router = Router(
    path="/wb",
    route_handlers=[PickupOrdersController, PickupMetaController],
)
