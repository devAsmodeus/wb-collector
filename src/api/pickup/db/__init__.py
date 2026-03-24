"""DB: Самовывоз (06)."""
from litestar import Router
from src.api.pickup.db.orders import DbPickupOrdersController

pickup_db_router = Router(
    path="/db",
    route_handlers=[DbPickupOrdersController],
)
