"""
Контроллер: FBS / Поставки и короба
WB API: marketplace-api.wildberries.ru

Поставка FBS — это партия товаров, передаваемая продавцом на склад WB.
Поставка содержит сборочные задания и может включать короба для удобства упаковки.
"""
from litestar import Controller, delete, get, patch, post
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.fbs.supplies import (
    AddBoxesRequest, AddOrdersToSupplyRequest,
    BoxStickersRequest, BoxStickersResponse, BoxesResponse,
    CreateSupplyRequest, CreateSupplyResponse,
    DeleteBoxesRequest, SuppliesResponse, SupplyBarcode,
    SupplyOrderIdsResponse,
)
from src.services.fbs.supplies import SuppliesService


class SuppliesController(Controller):
    path = "/supplies"
    tags = ["Поставки FBS"]

    @post(
        "/",
        summary="Создать поставку",
        description=(
            "Создаёт новую поставку FBS.\n\n"
            "После создания добавьте сборочные задания через `PATCH /fbs/supplies/{id}/orders`, "
            "затем передайте поставку в доставку через `PATCH /fbs/supplies/{id}/deliver`.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/supplies`"
        ),
    )
    async def create_supply(self, data: CreateSupplyRequest) -> CreateSupplyResponse:
        return await SuppliesService().create_supply(data)

    @get(
        "/",
        summary="Список поставок",
        description=(
            "Возвращает поставки продавца с пагинацией.\n\n"
            "Включает все поставки: активные, переданные в доставку и закрытые.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/supplies`"
        ),
    )
    async def get_supplies(
        self,
        limit: int = Parameter(
            1000,
            query="limit",
            ge=1,
            le=1000,
            description="Количество поставок в ответе. По умолчанию: 1000.",
        ),
        offset: int = Parameter(
            0,
            query="offset",
            ge=0,
            description="Смещение для пагинации. По умолчанию: 0.",
        ),
    ) -> SuppliesResponse:
        return await SuppliesService().get_supplies(limit=limit, offset=offset)

    @get(
        "/{supply_id:str}",
        summary="Информация о поставке",
        description=(
            "Возвращает детальную информацию о конкретной поставке по её ID.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/supplies/{supplyId}`"
        ),
    )
    async def get_supply(
        self,
        supply_id: str = Parameter(description="ID поставки (напр. `WB-GI-12345678`)"),
    ) -> dict:
        return await SuppliesService().get_supply(supply_id)

    @delete(
        "/{supply_id:str}",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить поставку",
        description=(
            "Удаляет поставку по её ID.\n\n"
            "Удалить можно только поставки, которые ещё не переданы в доставку.\n\n"
            "**WB endpoint:** `DELETE marketplace-api.wildberries.ru/api/v3/supplies/{supplyId}`"
        ),
    )
    async def delete_supply(
        self,
        supply_id: str = Parameter(description="ID поставки для удаления"),
    ) -> None:
        await SuppliesService().delete_supply(supply_id)

    @patch(
        "/{supply_id:str}/orders",
        status_code=HTTP_204_NO_CONTENT,
        summary="Добавить заказы в поставку",
        description=(
            "Добавляет сборочные задания в существующую поставку.\n\n"
            "Максимум **500 заданий** за один запрос.\n\n"
            "Задания должны быть в статусе `confirm`.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/marketplace/v3/supplies/{supplyId}/orders`"
        ),
    )
    async def add_orders_to_supply(
        self,
        data: AddOrdersToSupplyRequest,
        supply_id: str = Parameter(description="ID поставки"),
    ) -> None:
        await SuppliesService().add_orders_to_supply(supply_id, data)

    @get(
        "/{supply_id:str}/order-ids",
        summary="ID заказов в поставке",
        description=(
            "Возвращает список ID сборочных заданий, входящих в поставку.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/marketplace/v3/supplies/{supplyId}/order-ids`"
        ),
    )
    async def get_supply_order_ids(
        self,
        supply_id: str = Parameter(description="ID поставки"),
    ) -> SupplyOrderIdsResponse:
        return await SuppliesService().get_supply_order_ids(supply_id)

    @patch(
        "/{supply_id:str}/deliver",
        status_code=HTTP_204_NO_CONTENT,
        summary="Передать поставку в доставку",
        description=(
            "Закрывает поставку и передаёт её в доставку WB.\n\n"
            "После этого добавить или удалить заказы из поставки невозможно.\n\n"
            "Перед передачей убедитесь, что:\n"
            "- Все товары собраны и упакованы\n"
            "- На каждый товар наклеен стикер\n"
            "- Поставка содержит хотя бы одно сборочное задание\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/supplies/{supplyId}/deliver`"
        ),
    )
    async def deliver_supply(
        self,
        supply_id: str = Parameter(description="ID поставки для передачи в доставку"),
    ) -> None:
        await SuppliesService().deliver_supply(supply_id)

    @get(
        "/{supply_id:str}/barcode",
        summary="QR-код поставки",
        description=(
            "Возвращает QR-код поставки для сканирования при сдаче на склад WB.\n\n"
            "QR-код нужно распечатать и предъявить при въезде на склад.\n\n"
            "**Форматы:** `svg` — векторный (по умолчанию), `zplLabel` — для ZPL-принтеров.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/supplies/{supplyId}/barcode`"
        ),
    )
    async def get_supply_barcode(
        self,
        supply_id: str = Parameter(description="ID поставки"),
        barcode_type: str = Parameter(
            "svg",
            query="type",
            description="Формат QR-кода: `svg` (по умолчанию) или `zplLabel`.",
        ),
    ) -> SupplyBarcode:
        return await SuppliesService().get_supply_barcode(supply_id, barcode_type)

    @get(
        "/{supply_id:str}/boxes",
        summary="Список коробов поставки",
        description=(
            "Возвращает все короба, добавленные в поставку.\n\n"
            "Короба используются для укрупнённой упаковки при отгрузке большого количества товаров.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx`"
        ),
    )
    async def get_supply_boxes(
        self,
        supply_id: str = Parameter(description="ID поставки"),
    ) -> BoxesResponse:
        return await SuppliesService().get_supply_boxes(supply_id)

    @post(
        "/{supply_id:str}/boxes",
        summary="Добавить короба к поставке",
        description=(
            "Добавляет указанное количество коробов к поставке.\n\n"
            "Каждый короб получает уникальный ID (`WB-TRBX-XXXXXXXX`) и стикер для печати.\n\n"
            "Диапазон: 1–10 000 коробов за запрос.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx`"
        ),
    )
    async def add_boxes(
        self,
        data: AddBoxesRequest,
        supply_id: str = Parameter(description="ID поставки"),
    ) -> BoxesResponse:
        return await SuppliesService().add_boxes(supply_id, data)

    @delete(
        "/{supply_id:str}/boxes",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить короба из поставки",
        description=(
            "Удаляет указанные короба из поставки по их ID.\n\n"
            "**WB endpoint:** `DELETE marketplace-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx`"
        ),
    )
    async def delete_boxes(
        self,
        data: DeleteBoxesRequest,
        supply_id: str = Parameter(description="ID поставки"),
    ) -> None:
        await SuppliesService().delete_boxes(supply_id, data)

    @post(
        "/{supply_id:str}/boxes/stickers",
        summary="Стикеры для коробов",
        description=(
            "Возвращает стикеры для указанных коробов поставки.\n\n"
            "Стикеры нужно распечатать и наклеить на каждый короб перед сдачей поставки.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx/stickers`"
        ),
    )
    async def get_box_stickers(
        self,
        data: BoxStickersRequest,
        supply_id: str = Parameter(description="ID поставки"),
        sticker_type: str = Parameter(
            "png",
            query="type",
            description="Формат стикера: `png` (по умолчанию) или `svg`.",
        ),
    ) -> BoxStickersResponse:
        return await SuppliesService().get_box_stickers(supply_id, data, sticker_type)
