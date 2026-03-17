"""Router: Самовывоз (06) — Click & Collect (28 endpoints)."""
from litestar import Router

from src.api.pickup.orders import PickupOrdersController
from src.api.pickup.meta import PickupMetaController

pickup_router = Router(
    path="/pickup",
    route_handlers=[PickupOrdersController, PickupMetaController],
)
