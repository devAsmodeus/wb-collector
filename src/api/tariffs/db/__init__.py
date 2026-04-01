"""DB: Tariffs (10) — Тарифы."""
from litestar import Router
from src.api.tariffs.db.tariffs import DbCommissionsController, DbBoxController, DbPalletController, DbSupplyController

tariffs_db_router = Router(
    path="/db",
    route_handlers=[DbCommissionsController, DbBoxController, DbPalletController, DbSupplyController],
)
