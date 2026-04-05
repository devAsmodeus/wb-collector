"""DB: FBS (03)."""
from litestar import Router
from src.api.fbs.db.orders import DbFbsOrdersController
from src.api.fbs.db.supplies import DbFbsSuppliesController
from src.api.fbs.db.passes import DbFbsPassesController

fbs_db_router = Router(
    path="/db",
    route_handlers=[DbFbsOrdersController, DbFbsSuppliesController, DbFbsPassesController],
)
