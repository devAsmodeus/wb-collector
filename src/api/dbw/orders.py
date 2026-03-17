"""
Контроллер: DBW / Сборочные задания
WB API: marketplace-api.wildberries.ru
Tag: Сборочные задания DBW (10 endpoints)

DBW (Доставка WB) — модель, при которой курьер WB забирает товар
у продавца и доставляет покупателю.
"""
from litestar import Controller, get, patch, post
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.dbw.orders import (
    DBWClientOrdersRequest, DBWCourierRequest, DBWDeliveryDateRequest,
    DBWOrderStatusRequest, DBWOrderStatusResponse,
    DBWOrdersResponse, DBWStickersRequest, DBWStickersResponse,
)
from src.services.dbw.orders import DBWOrdersService


class DBWOrdersController(Controller):
    path = "/orders"
    tags = ["Сборочные задания DBW"]

    @get(
        "/new",
        summary="Получить список новых сборочных заданий",
        description=(
            "Возвращает новые сборочные задания DBW, ожидающие подтверждения продавцом.\n\n"
            "**Важно:** проверяйте поле `requiredMeta` — обязательные метаданные "
            "нужно заполнить до передачи задания в доставку.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/dbw/orders/new`"
        ),
    )
    async def get_new_orders(self) -> DBWOrdersResponse:
        return await DBWOrdersService().get_new_orders()

    @get(
        "/",
        summary="Получить информацию о сборочных заданиях",
        description=(
            "Возвращает сборочные задания DBW за указанный период.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/dbw/orders`"
        ),
    )
    async def get_orders(
        self,
        date_from: int | None = Parameter(
            None, query="date_from",
            description="Дата начала периода, Unix timestamp (сек).",
        ),
        date_to: int | None = Parameter(
            None, query="date_to",
            description="Дата конца периода, Unix timestamp (сек).",
        ),
    ) -> DBWOrdersResponse:
        return await DBWOrdersService().get_orders(date_from=date_from, date_to=date_to)

    @post(
        "/delivery-date",
        status_code=HTTP_204_NO_CONTENT,
        summary="Установить дату доставки",
        description=(
            "Устанавливает планируемую дату доставки покупателю для заданий DBW.\n\n"
            "Дата отображается покупателю при отслеживании заказа.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/dbw/orders/delivery-date`"
        ),
    )
    async def set_delivery_date(self, data: DBWDeliveryDateRequest) -> None:
        await DBWOrdersService().set_delivery_date(data)

    @post(
        "/client",
        summary="Заказы с информацией по клиенту",
        description=(
            "Возвращает сборочные задания DBW с дополнительными данными о покупателе.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbw/orders/client`"
        ),
    )
    async def get_client_orders(self, data: DBWClientOrdersRequest) -> dict:
        return await DBWOrdersService().get_client_orders(data)

    @post(
        "/status",
        summary="Получить статусы сборочных заданий",
        description=(
            "Возвращает текущие статусы (`supplierStatus`, `wbStatus`) "
            "для переданного списка заданий DBW.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/dbw/orders/status`"
        ),
    )
    async def get_orders_status(self, data: DBWOrderStatusRequest) -> DBWOrderStatusResponse:
        return await DBWOrdersService().get_orders_status(data)

    @patch(
        "/{order_id:int}/confirm",
        status_code=HTTP_204_NO_CONTENT,
        summary="Подтвердить сборочное задание",
        description=(
            "Подтверждает готовность к сборке задания DBW.\n\n"
            "После подтверждения задание переходит в статус `confirm`.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/confirm`"
        ),
    )
    async def confirm_order(
        self,
        order_id: int = Parameter(description="ID сборочного задания для подтверждения"),
    ) -> None:
        await DBWOrdersService().confirm_order(order_id)

    @post(
        "/stickers",
        summary="Получить стикеры сборочных заданий",
        description=(
            "Возвращает стикеры (этикетки) для заданий DBW.\n\n"
            "**Форматы:** `png` (по умолчанию) или `svg`.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/dbw/orders/stickers`"
        ),
    )
    async def get_stickers(
        self,
        data: DBWStickersRequest,
        sticker_type: str = Parameter("png", query="type", description="Формат стикера: `png` или `svg`."),
        width: int = Parameter(58, query="width", description="Ширина стикера в мм."),
        height: int = Parameter(40, query="height", description="Высота стикера в мм."),
    ) -> DBWStickersResponse:
        return await DBWOrdersService().get_stickers(data, sticker_type, width, height)

    @patch(
        "/{order_id:int}/assemble",
        status_code=HTTP_204_NO_CONTENT,
        summary="Отметить задание как собранное",
        description=(
            "Переводит задание DBW в статус `assembled` — товар собран и готов к передаче курьеру.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/assemble`"
        ),
    )
    async def assemble_order(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> None:
        await DBWOrdersService().assemble_order(order_id)

    @post(
        "/courier",
        status_code=HTTP_204_NO_CONTENT,
        summary="Вызвать курьера WB",
        description=(
            "Вызывает курьера WB для забора собранных заданий DBW.\n\n"
            "Передавайте только задания в статусе `assembled`.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/dbw/orders/courier`"
        ),
    )
    async def call_courier(self, data: DBWCourierRequest) -> None:
        await DBWOrdersService().call_courier(data)

    @patch(
        "/{order_id:int}/cancel",
        status_code=HTTP_204_NO_CONTENT,
        summary="Отменить сборочное задание",
        description=(
            "Отменяет задание DBW. Возможно только до передачи курьеру.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/cancel`"
        ),
    )
    async def cancel_order(
        self,
        order_id: int = Parameter(description="ID сборочного задания для отмены"),
    ) -> None:
        await DBWOrdersService().cancel_order(order_id)
