"""DB: Reports — Чтение отчётов WB из БД."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.reports.db.reports import ReportsDbService
from src.utils.db_manager import DBManager


class DbStocksController(Controller):
    path = "/stocks"
    tags = ["12. База данных"]

    @get(
        "/",
        summary="Остатки на складах из БД",
        description=(
            "Возвращает остатки товаров из таблицы `wb_stocks`.\n\n"
            "Перед первым вызовом выполните `POST /reports/sync/stocks/`."
        ),
    )
    async def get_stocks(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Фильтр дата от"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Фильтр дата до"),
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsDbService().get_stocks(db.session, date_from=date_from, date_to=date_to, limit=limit, offset=offset)


class DbOrdersController(Controller):
    path = "/orders"
    tags = ["12. База данных"]

    @get(
        "/",
        summary="Заказы из БД",
        description=(
            "Возвращает заказы из таблицы `wb_orders_report`.\n\n"
            "Перед первым вызовом выполните `POST /reports/sync/orders/`."
        ),
    )
    async def get_orders(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Фильтр дата от"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Фильтр дата до"),
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsDbService().get_orders(db.session, date_from=date_from, date_to=date_to, limit=limit, offset=offset)


class DbSalesController(Controller):
    path = "/sales"
    tags = ["12. База данных"]

    @get(
        "/",
        summary="Продажи и возвраты из БД",
        description=(
            "Возвращает продажи и возвраты из таблицы `wb_sales_report`.\n\n"
            "Перед первым вызовом выполните `POST /reports/sync/sales/`."
        ),
    )
    async def get_sales(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Фильтр дата от"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Фильтр дата до"),
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await ReportsDbService().get_sales(db.session, date_from=date_from, date_to=date_to, limit=limit, offset=offset)
