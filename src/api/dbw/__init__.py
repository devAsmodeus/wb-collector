"""Router: DBW (04) — Заказы DBW (16 endpoints)."""
from litestar import Router

from src.api.dbw.orders import DBWOrdersController
from src.api.dbw.meta import DBWMetaController

dbw_router = Router(
    path="/dbw",
    route_handlers=[DBWOrdersController, DBWMetaController],
)
