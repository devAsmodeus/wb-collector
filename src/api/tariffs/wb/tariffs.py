"""
Контроллер WB: Тарифы WB (10)
WB API: common-api.wildberries.ru
Tags: Комиссии, Стоимость возврата продавцу, Тарифы на остаток, Тарифы на поставку (5 ep)
"""
from litestar import Controller, get
from litestar.params import Parameter

from src.services.tariffs.wb.tariffs import TariffsWbService


class TariffsWbController(Controller):
    path = "/tariffs"
    tags = ["10. API Wildberries"]

    @get(
        "/commission",
        tags=["10. API Wildberries"],
        summary="Комиссии по категориям товаров",
        description=(
            "Возвращает список комиссий WB по категориям товаров для всех схем работы.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/v1/tariffs/commission`"
        ),
    )
    async def get_commissions(self) -> dict:
        return await TariffsWbService().get_commissions()

    @get(
        "/seller",
        tags=["10. API Wildberries"],
        summary="Стоимость возврата товаров продавцу",
        description=(
            "Возвращает тарифы стоимости возврата товаров продавцу со складов WB.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/v1/tariffs/seller`"
        ),
    )
    async def get_return_cost(
        self,
        date: str | None = Parameter(None, query="date", description="Дата для получения тарифов в формате `YYYY-MM-DD`. По умолчанию — текущая."),
    ) -> dict:
        return await TariffsWbService().get_return_cost(date)

    @get(
        "/box",
        tags=["10. API Wildberries"],
        summary="Тарифы на доставку и хранение коробами",
        description=(
            "Возвращает тарифы на доставку и хранение товаров в коробах по складам WB.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/v1/tariffs/box`"
        ),
    )
    async def get_box_tariffs(
        self,
        date: str | None = Parameter(None, query="date", description="Дата тарифов в формате `YYYY-MM-DD`. По умолчанию — текущая."),
    ) -> dict:
        return await TariffsWbService().get_box_tariffs(date)

    @get(
        "/pallet",
        tags=["10. API Wildberries"],
        summary="Тарифы на доставку и хранение паллетами",
        description=(
            "Возвращает тарифы на доставку и хранение товаров на паллетах по складам WB.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/v1/tariffs/pallet`"
        ),
    )
    async def get_pallet_tariffs(
        self,
        date: str | None = Parameter(None, query="date", description="Дата тарифов в формате `YYYY-MM-DD`. По умолчанию — текущая."),
    ) -> dict:
        return await TariffsWbService().get_pallet_tariffs(date)

    @get(
        "/supply",
        tags=["10. API Wildberries"],
        summary="Коэффициенты складов для поставок",
        description=(
            "Возвращает коэффициенты складов WB для расчёта стоимости поставок.\n\n"
            "Коэффициент `0` — бесплатная приёмка, `-1` — склад закрыт для поставок.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/v1/tariffs/warehouseCoeff`"
        ),
    )
    async def get_supply_tariffs(
        self,
        date: str | None = Parameter(None, query="date", description="Дата тарифов в формате `YYYY-MM-DD`. По умолчанию — текущая."),
    ) -> dict:
        return await TariffsWbService().get_supply_tariffs(date)
