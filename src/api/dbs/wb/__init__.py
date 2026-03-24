"""WB API proxy: DBS (05) — Сборочные задания DBS."""
from litestar import Router

from src.api.dbs.wb.orders import DBSOrdersController
from src.api.dbs.wb.meta import DBSMetaController

dbs_wb_router = Router(
    path="/wb",
    route_handlers=[DBSOrdersController, DBSMetaController],
)
