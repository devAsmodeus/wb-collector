"""DB: General (01)."""
from litestar import Router
from src.api.db.general.seller import DbSellerController
from src.api.db.general.news import DbNewsController

db_general_router = Router(
    path="/general",
    route_handlers=[DbSellerController, DbNewsController],
)
