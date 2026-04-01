"""Sync: Products (02)."""
from litestar import Router
from src.api.products.sync.cards import SyncCardsController
from src.api.products.sync.prices import SyncPricesController
from src.api.products.sync.tags import SyncTagsController
from src.api.products.sync.warehouses import SyncWarehousesController
from src.api.products.sync.directories import SyncDirectoriesController

products_sync_router = Router(
    path="/sync",
    route_handlers=[
        SyncCardsController, SyncPricesController, SyncTagsController,
        SyncWarehousesController, SyncDirectoriesController,
    ],
)
