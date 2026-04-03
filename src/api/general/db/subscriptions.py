"""DB: General / Подписки Джем."""
from litestar import Controller, get
from src.schemas.general.subscriptions import SubscriptionsJamInfo
from src.services.general.db.subscriptions import SubscriptionsDbService
from src.utils.db_manager import DBManager


class DbSubscriptionsController(Controller):
    path = "/subscriptions"
    tags = ["01. База данных"]

    @get(
        "/",
        summary="Подписки Джем из БД",
        description=(
            "Возвращает подписки Джем из таблицы `wb_seller_subscriptions`.\n\n"
            "Перед первым вызовом выполните `POST /general/sync/subscriptions/full`."
        ),
    )
    async def get_subscriptions(self) -> SubscriptionsJamInfo | None:
        async with DBManager() as db:
            return await SubscriptionsDbService().get_subscriptions(db.session)
