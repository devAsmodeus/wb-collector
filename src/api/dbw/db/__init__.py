"""DB: DBW (04)."""
from litestar import Router
from src.api.dbw.db.orders import DbDBWOrdersController

dbw_db_router = Router(
    path="/db",
    route_handlers=[DbDBWOrdersController],
)
