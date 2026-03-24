"""
Контроллер: FBW / Информация для формирования поставок
WB API: marketplace-api.wildberries.ru
Tag: Информация для формирования поставок (3 endpoints)
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.fbw.acceptance import (
    FBWAcceptanceOptionsRequest, FBWTransitTariffsResponse, FBWWarehousesResponse,
)
from src.services.fbw.wb.acceptance import FBWAcceptanceService


class FBWAcceptanceController(Controller):
    path = "/"
    tags = ["Информация для формирования поставок"]

    @post(
        "/acceptance/options",
        summary="Опции приёмки",
        description=(
            "Возвращает доступные опции приёмки (склады, типы поставок, тарифы) "
            "для указанного списка товаров.\n\n"
            "Передайте массив товаров с баркодами и количеством — получите, "
            "на какие склады и каким способом можно отгрузить товар.\n\n"
            "Максимум **5000 позиций** в запросе.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v1/acceptance/options`"
        ),
    )
    async def get_acceptance_options(
        self,
        data: FBWAcceptanceOptionsRequest,
        warehouse_id: int | None = Parameter(
            None,
            query="warehouseID",
            description="ID склада WB для фильтрации. Если не указан — возвращаются данные по всем складам.",
        ),
    ) -> dict:
        return await FBWAcceptanceService().get_acceptance_options(data, warehouse_id)

    @get(
        "/warehouses",
        summary="Список складов",
        description=(
            "Возвращает список складов WB, принимающих FBW-поставки.\n\n"
            "Используйте для получения актуального списка складов и их ID "
            "перед формированием поставки.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v1/warehouses`"
        ),
    )
    async def get_warehouses(self) -> FBWWarehousesResponse:
        return await FBWAcceptanceService().get_warehouses()

    @get(
        "/transit-tariffs",
        summary="Тарифы транзитной доставки",
        description=(
            "Возвращает тарифы транзитной доставки между складами WB.\n\n"
            "Содержит поля:\n"
            "- `boxTariff` — тариф за транзит коробов (руб. за коробку)\n"
            "- `palletTariff` — тариф за паллету (руб.)\n"
            "- `isBoxOnPallet` — флаг типа поставки «Поштучная паллета»\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v1/transit-tariffs`"
        ),
    )
    async def get_transit_tariffs(self) -> FBWTransitTariffsResponse:
        return await FBWAcceptanceService().get_transit_tariffs()
