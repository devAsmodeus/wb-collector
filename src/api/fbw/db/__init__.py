"""DB: FBW (07) — Поставки FBW."""
from litestar import Router
from src.api.fbw.db.warehouses import DbFbwWarehousesController
from src.api.fbw.db.transit_tariffs import DbFbwTransitTariffsController
from src.api.fbw.db.supplies import DbFbwSuppliesController

fbw_db_router = Router(
    path="/db",
    route_handlers=[
        DbFbwWarehousesController,
        DbFbwTransitTariffsController,
        DbFbwSuppliesController,
    ],
)
