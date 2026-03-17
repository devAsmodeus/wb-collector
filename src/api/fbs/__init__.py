"""Router: FBS (03) — Заказы FBS (34 endpoints)."""
from litestar import Router

from src.api.fbs.passes import PassesController
from src.api.fbs.orders import OrdersController
from src.api.fbs.meta import MetaController
from src.api.fbs.supplies import SuppliesController

fbs_router = Router(
    path="/fbs",
    route_handlers=[PassesController, OrdersController, MetaController, SuppliesController],
)
