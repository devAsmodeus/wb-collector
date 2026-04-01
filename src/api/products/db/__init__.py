"""DB: Products (02)."""
from litestar import Router
from src.api.products.db.cards import DbCardsController
from src.api.products.db.prices import DbPricesController
from src.api.products.db.tags import DbTagsController
from src.api.products.db.warehouses import DbWarehousesController
from src.api.products.db.directories import DbDirectoriesController

products_db_router = Router(
    path="/db",
    route_handlers=[
        DbCardsController, DbPricesController, DbTagsController,
        DbWarehousesController, DbDirectoriesController,
    ],
)
