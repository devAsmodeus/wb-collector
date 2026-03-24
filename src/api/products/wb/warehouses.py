"""
Контроллер: Products / Склады и остатки
WB API: marketplace-api.wildberries.ru

Склады WB (офисы приёмки), склады продавца и остатки товаров.
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.products.warehouses import (
    SellerWarehousesResponse,
    StocksRequest,
    StocksResponse,
    WBOfficesResponse,
)
from src.services.products.wb.warehouses import WarehousesService


class WarehousesController(Controller):
    path = "/warehouses"
    tags = ["Products — Склады"]

    @get(
        "/wb",
        summary="Склады WB (офисы приёмки)",
        description=(
            "Возвращает список всех складов WB — точек приёмки товара от продавца.\n\n"
            "Используется при создании поставки (FBW): нужно выбрать склад WB, "
            "на который будет отгружен товар.\n\n"
            "Каждый склад содержит название, адрес, город и координаты.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/offices`"
        ),
    )
    async def get_wb_offices(self) -> WBOfficesResponse:
        return await WarehousesService().get_wb_offices()

    @get(
        "/",
        summary="Склады продавца",
        description=(
            "Возвращает список собственных складов продавца (схема FBS).\n\n"
            "Для каждого склада указан:\n"
            "- `officeId` — к какому офису WB привязан\n"
            "- `cargoType` — тип упаковки (короба / паллеты / суперсейф)\n"
            "- `isProcessing` — активен ли склад сейчас\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/warehouses`"
        ),
    )
    async def get_seller_warehouses(self) -> SellerWarehousesResponse:
        return await WarehousesService().get_seller_warehouses()

    @post(
        "/{warehouse_id:int}/stocks",
        summary="Остатки товаров на складе продавца",
        description=(
            "Возвращает остатки товаров на указанном складе продавца по списку баркодов.\n\n"
            "**Важно:** метод работает только для FBS-складов продавца, "
            "не для складов WB.\n\n"
            "За один запрос можно передать до **1000 баркодов**.\n\n"
            "Если баркод не найден на складе — он не будет включён в ответ "
            "(отсутствие = 0 остатков).\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/warehouses/{warehouseId}/stocks`"
        ),
    )
    async def get_stocks(
        self,
        data: StocksRequest,
        warehouse_id: int = Parameter(
            description="ID склада продавца (из `/warehouses`).",
        ),
    ) -> StocksResponse:
        return await WarehousesService().get_stocks(
            warehouse_id=warehouse_id,
            skus=data.skus,
        )
