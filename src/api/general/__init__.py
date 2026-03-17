"""Router: General (01) — Общее."""
from litestar import Router

from src.api.general.seller import SellerController
from src.api.general.news import NewsController
from src.api.general.users import UsersController

general_router = Router(
    path="/general",
    route_handlers=[SellerController, NewsController, UsersController],
)
