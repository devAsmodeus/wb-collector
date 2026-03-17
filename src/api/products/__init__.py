"""Router: Products (02) — Товары."""
from litestar import Router

from src.api.products.directories import DirectoriesController
from src.api.products.tags import TagsController
from src.api.products.cards import CardsController, BarcodesController
from src.api.products.media import MediaController
from src.api.products.prices import PricesController
from src.api.products.warehouses import WarehousesController

products_router = Router(
    path="/products",
    route_handlers=[
        DirectoriesController,
        TagsController,
        CardsController,
        BarcodesController,
        MediaController,
        PricesController,
        WarehousesController,
    ],
)
