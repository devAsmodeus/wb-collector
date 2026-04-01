"""Sync: FBW (07) — Поставки FBW."""
from litestar import Router
from src.api.fbw.sync.warehouses import SyncFbwWarehousesController
from src.api.fbw.sync.transit_tariffs import SyncFbwTransitTariffsController
from src.api.fbw.sync.supplies import SyncFbwSuppliesController

fbw_sync_router = Router(
    path="/sync",
    route_handlers=[
        SyncFbwWarehousesController,
        SyncFbwTransitTariffsController,
        SyncFbwSuppliesController,
    ],
)
