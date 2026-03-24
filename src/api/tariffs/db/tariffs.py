"""DB: Tariffs — Чтение тарифов WB из БД."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.tariffs.db.tariffs import TariffsDbService
from src.utils.db_manager import DBManager


class DbCommissionsController(Controller):
    path = "/commissions"
    tags = ["DB / Tariffs"]

    @get(
        "/",
        summary="Комиссии по категориям из БД",
        description=(
            "Возвращает комиссии WB по категориям из таблицы `wb_tariffs_commission`.\n\n"
            "Перед первым вызовом выполните `POST /tariffs/sync/commissions/`."
        ),
    )
    async def get_commissions(
        self,
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await TariffsDbService().get_commissions(db.session, limit=limit, offset=offset)


class DbBoxController(Controller):
    path = "/box"
    tags = ["DB / Tariffs"]

    @get(
        "/",
        summary="Тарифы коробами из БД",
        description=(
            "Возвращает тарифы на доставку и хранение коробами из таблицы `wb_tariffs_box`.\n\n"
            "Перед первым вызовом выполните `POST /tariffs/sync/box/`."
        ),
    )
    async def get_box_tariffs(
        self,
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await TariffsDbService().get_box_tariffs(db.session, limit=limit, offset=offset)


class DbPalletController(Controller):
    path = "/pallet"
    tags = ["DB / Tariffs"]

    @get(
        "/",
        summary="Тарифы паллетами из БД",
        description=(
            "Возвращает тарифы на доставку и хранение паллетами из таблицы `wb_tariffs_pallet`.\n\n"
            "Перед первым вызовом выполните `POST /tariffs/sync/pallet/`."
        ),
    )
    async def get_pallet_tariffs(
        self,
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await TariffsDbService().get_pallet_tariffs(db.session, limit=limit, offset=offset)


class DbSupplyController(Controller):
    path = "/supply"
    tags = ["DB / Tariffs"]

    @get(
        "/",
        summary="Коэффициенты поставок из БД",
        description=(
            "Возвращает коэффициенты складов для поставок из таблицы `wb_tariffs_supply`.\n\n"
            "Перед первым вызовом выполните `POST /tariffs/sync/supply/`."
        ),
    )
    async def get_supply_tariffs(
        self,
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await TariffsDbService().get_supply_tariffs(db.session, limit=limit, offset=offset)
