"""Sync: Tariffs (10) — Тарифы."""
from litestar import Router
from src.api.tariffs.sync.tariffs import SyncCommissionsController, SyncBoxController, SyncPalletController, SyncSupplyController

tariffs_sync_router = Router(
    path="/sync",
    route_handlers=[SyncCommissionsController, SyncBoxController, SyncPalletController, SyncSupplyController],
)
