"""DB: General (01)."""
from litestar import Router
from src.api.general.db.seller import DbSellerController
from src.api.general.db.news import DbNewsController

general_db_router = Router(
    path="/db",
    route_handlers=[DbSellerController, DbNewsController],
)
