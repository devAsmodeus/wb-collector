"""WB API proxy: Products (02) — Товары."""
from litestar import Router

from src.api.products.wb.directories import DirectoriesController
from src.api.products.wb.tags import TagsController
from src.api.products.wb.cards import CardsController, BarcodesController
from src.api.products.wb.media import MediaController
from src.api.products.wb.prices import PricesController
from src.api.products.wb.warehouses import WBOfficesController, SellerWarehousesController

products_wb_router = Router(
    path="/wb",
    route_handlers=[
        DirectoriesController, TagsController, CardsController, BarcodesController,
        MediaController, PricesController, WBOfficesController, SellerWarehousesController,
    ],
)
