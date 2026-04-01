"""WB API proxy: DBW (04) — Сборочные задания DBW."""
from litestar import Router

from src.api.dbw.wb.orders import DBWOrdersController
from src.api.dbw.wb.meta import DBWMetaController

dbw_wb_router = Router(
    path="/wb",
    route_handlers=[DBWOrdersController, DBWMetaController],
)
