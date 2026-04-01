"""
Контроллер: FBW / Информация о поставках
WB API: marketplace-api.wildberries.ru
Tag: Информация о поставках (4 endpoints)
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.fbw.supplies import (
    FBWPackageQR, FBWSuppliesFiltersRequest,
    FBWSuppliesResponse, FBWSupplyGoodsResponse,
)
from src.services.fbw.wb.supplies import FBWSuppliesService


class FBWSuppliesController(Controller):
    path = "/supplies"
    tags = ["07. API Wildberries"]

    @post(
        "/",
        summary="Список поставок",
        description=(
            "Возвращает список FBW-поставок с возможностью фильтрации по датам и статусам.\n\n"
            "**Статусы:** `1` — Не запланировано, `2` — Запланировано, "
            "`3` — В пути, `4` — Принято, `5` — Отклонено.\n\n"
            "Содержит новые поля:\n"
            "- `boxTypeID` — ID типа поставки (0–5)\n"
            "- `isBoxOnPallet` — поставка типа «Поштучная паллета»\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v1/supplies`"
        ),
    )
    async def get_supplies(
        self,
        data: FBWSuppliesFiltersRequest,
        limit: int = Parameter(
            1000, query="limit", ge=1, le=5000,
            description="Количество записей в ответе (1–5000). По умолчанию: 1000.",
        ),
        offset: int = Parameter(
            0, query="offset", ge=0,
            description="Смещение для пагинации. По умолчанию: 0.",
        ),
    ) -> FBWSuppliesResponse:
        return await FBWSuppliesService().get_supplies(data, limit, offset)

    @get(
        "/{supply_id:int}",
        summary="Детали поставки",
        description=(
            "Возвращает подробную информацию о поставке FBW по её ID.\n\n"
            "Поддерживает поиск как по ID поставки (`supplyID`), "
            "так и по ID заказа (`preorderID`) — используйте параметр `isPreorderID`.\n\n"
            "Содержит поля `boxTypeID` и `isBoxOnPallet`.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v1/supplies/{ID}`"
        ),
    )
    async def get_supply(
        self,
        supply_id: int = Parameter(description="ID поставки или ID заказа (в зависимости от `isPreorderID`)"),
        is_preorder_id: bool = Parameter(
            False, query="isPreorderID",
            description="`true` — искать по ID заказа (`preorderID`), `false` — по ID поставки (по умолчанию).",
        ),
    ) -> dict:
        return await FBWSuppliesService().get_supply(supply_id, is_preorder_id)

    @get(
        "/{supply_id:int}/goods",
        summary="Товары поставки",
        description=(
            "Возвращает список товаров в составе поставки FBW с пагинацией.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v1/supplies/{ID}/goods`"
        ),
    )
    async def get_supply_goods(
        self,
        supply_id: int = Parameter(description="ID поставки или ID заказа"),
        limit: int = Parameter(1000, query="limit", ge=1, le=5000, description="Количество записей. По умолчанию: 1000."),
        offset: int = Parameter(0, query="offset", ge=0, description="Смещение. По умолчанию: 0."),
        is_preorder_id: bool = Parameter(False, query="isPreorderID", description="`true` — поиск по ID заказа."),
    ) -> FBWSupplyGoodsResponse:
        return await FBWSuppliesService().get_supply_goods(supply_id, limit, offset, is_preorder_id)

    @get(
        "/{supply_id:int}/package",
        summary="QR-код упаковки поставки",
        description=(
            "Возвращает QR-код для упаковки поставки FBW.\n\n"
            "QR-код необходимо распечатать и разместить на упаковке поставки перед сдачей на склад WB.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v1/supplies/{ID}/package`"
        ),
    )
    async def get_supply_package(
        self,
        supply_id: int = Parameter(description="ID поставки FBW"),
    ) -> FBWPackageQR:
        return await FBWSuppliesService().get_supply_package(supply_id)
