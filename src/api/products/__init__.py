"""Router: Products (02) — Товары."""
from litestar import Router

from src.api.products.wb import products_wb_router
from src.api.products.sync import products_sync_router
from src.api.products.db import products_db_router

products_router = Router(
    path="/products",
    route_handlers=[products_wb_router, products_sync_router, products_db_router],
)
