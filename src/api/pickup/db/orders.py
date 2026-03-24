"""DB: Самовывоз / Сборочные задания."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.pickup.db.orders import PickupOrdersDbService
from src.utils.db_manager import DBManager


class DbPickupOrdersController(Controller):
    path = "/orders"
    tags = ["DB / Pickup"]

    @get(
        "/",
        summary="Заказы Самовывоз из БД",
        description=(
            "Возвращает заказы Самовывоз из таблицы `pickup_orders` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /pickup/sync/orders/full`."
        ),
    )
    async def get_orders(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Дата начала (ISO 8601)"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Дата конца (ISO 8601)"),
        status: str | None = Parameter(default=None, query="status", description="Фильтр по supplierStatus"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await PickupOrdersDbService().get_orders(
                db.session,
                date_from=date_from,
                date_to=date_to,
                status=status,
                limit=limit,
                offset=offset,
            )
