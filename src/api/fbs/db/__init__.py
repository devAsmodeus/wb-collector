"""DB: FBS (03)."""
from litestar import Router
from src.api.fbs.db.orders import DbFbsOrdersController

fbs_db_router = Router(
    path="/db",
    route_handlers=[DbFbsOrdersController],
)
