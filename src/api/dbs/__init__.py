"""Router: DBS (05) — Заказы DBS (32 endpoints)."""
from litestar import Router

from src.api.dbs.orders import DBSOrdersController
from src.api.dbs.meta import DBSMetaController

dbs_router = Router(
    path="/dbs",
    route_handlers=[DBSOrdersController, DBSMetaController],
)
