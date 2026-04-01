"""DB: DBS (05)."""
from litestar import Router
from src.api.dbs.db.orders import DbDBSOrdersController

dbs_db_router = Router(
    path="/db",
    route_handlers=[DbDBSOrdersController],
)
