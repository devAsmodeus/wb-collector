"""WB API proxy: FBS (03) — Заказы FBS."""
from litestar import Router

from src.api.fbs.wb.orders import OrdersController
from src.api.fbs.wb.passes import PassesController
from src.api.fbs.wb.meta import MetaController
from src.api.fbs.wb.supplies import SuppliesController

fbs_wb_router = Router(
    path="/wb",
    route_handlers=[PassesController, OrdersController, MetaController, SuppliesController],
)
