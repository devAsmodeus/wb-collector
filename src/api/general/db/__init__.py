"""DB: General (01)."""
from litestar import Router
from src.api.general.db.seller import DbSellerController
from src.api.general.db.news import DbNewsController
from src.api.general.db.rating import DbRatingController
from src.api.general.db.subscriptions import DbSubscriptionsController
from src.api.general.db.users import DbUsersController

general_db_router = Router(
    path="/db",
    route_handlers=[
        DbSellerController,
        DbNewsController,
        DbRatingController,
        DbSubscriptionsController,
        DbUsersController,
    ],
)
