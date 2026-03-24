"""
Контроллер: DBS / Сборочные задания
WB API: marketplace-api.wildberries.ru
Tag: Сборочные задания DBS (19 endpoints, из них 5 deprecated)

DBS — продавец доставляет товар покупателю самостоятельно через свою службу доставки.
"""
from litestar import Controller, get, patch, post
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.dbs.orders import (
    DBSDeliveryDateRequest, DBSGroupInfoRequest,
    DBSOrderIdsRequest, DBSOrderStatusResponse,
    DBSOrdersResponse, DBSReceiveRequest,
    DBSRejectRequest, DBSStickersResponse,
)
from src.services.dbs.wb.orders import DBSOrdersService


class DBSOrdersController(Controller):
    path = "/orders"
    tags = ["Сборочные задания DBS"]

    @get(
        "/new",
        summary="Получить список новых сборочных заданий",
        description=(
            "Возвращает новые задания DBS, ожидающие подтверждения.\n\n"
            "Проверяйте `requiredMeta` — обязательные метаданные нужно заполнить до передачи в доставку.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/dbs/orders/new`"
        ),
    )
    async def get_new_orders(self) -> DBSOrdersResponse:
        return await DBSOrdersService().get_new_orders()

    @get(
        "/",
        summary="Получить информацию о завершённых сборочных заданиях",
        description=(
            "Возвращает завершённые задания DBS за указанный период.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/dbs/orders`"
        ),
    )
    async def get_orders(
        self,
        date_from: int | None = Parameter(None, query="date_from", description="Начало периода, Unix timestamp (сек)."),
        date_to: int | None = Parameter(None, query="date_to", description="Конец периода, Unix timestamp (сек)."),
    ) -> DBSOrdersResponse:
        return await DBSOrdersService().get_orders(date_from=date_from, date_to=date_to)

    @post(
        "/group-info",
        summary="Получить информацию о платной доставке",
        description=(
            "Возвращает данные о тарифе платной доставки для указанных заданий DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/dbs/groups/info`"
        ),
    )
    async def get_group_info(self, data: DBSGroupInfoRequest) -> dict:
        return await DBSOrdersService().get_group_info(data)

    @post(
        "/client",
        summary="Информация о покупателе",
        description=(
            "Возвращает данные покупателя для указанных заданий DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/dbs/orders/client`"
        ),
    )
    async def get_client_orders(self, data: DBSOrderIdsRequest) -> dict:
        return await DBSOrdersService().get_client_orders(data)

    @post(
        "/b2b-info",
        summary="Информация о покупателе B2B",
        description=(
            "Возвращает данные покупателя B2B для указанных заданий DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/b2b/info`"
        ),
    )
    async def get_b2b_info(self, data: DBSOrderIdsRequest) -> dict:
        return await DBSOrdersService().get_b2b_info(data)

    @post(
        "/delivery-date",
        status_code=HTTP_204_NO_CONTENT,
        summary="Дата и время доставки",
        description=(
            "Устанавливает планируемую дату и время доставки покупателю.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/dbs/orders/delivery-date`"
        ),
    )
    async def set_delivery_date(self, data: DBSDeliveryDateRequest) -> None:
        await DBSOrdersService().set_delivery_date(data)

    @post(
        "/status",
        summary="Получить статусы сборочных заданий",
        description=(
            "Возвращает статусы (`supplierStatus`, `wbStatus`) для списка заданий DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/status/info`"
        ),
    )
    async def get_orders_status(self, data: DBSOrderIdsRequest) -> DBSOrderStatusResponse:
        return await DBSOrdersService().get_orders_status(data)

    @post(
        "/cancel",
        status_code=HTTP_204_NO_CONTENT,
        summary="Отменить сборочные задания",
        description=(
            "Массово отменяет сборочные задания DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/status/cancel`"
        ),
    )
    async def cancel_orders(self, data: DBSOrderIdsRequest) -> None:
        await DBSOrdersService().cancel_orders(data)

    @post(
        "/confirm",
        status_code=HTTP_204_NO_CONTENT,
        summary="Перевести сборочные задания на сборку",
        description=(
            "Массово переводит задания DBS в статус `confirm` (на сборку).\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/status/confirm`"
        ),
    )
    async def confirm_orders(self, data: DBSOrderIdsRequest) -> None:
        await DBSOrdersService().confirm_orders(data)

    @post(
        "/stickers",
        summary="Получить стикеры для сборочных заданий с доставкой в ПВЗ",
        description=(
            "Возвращает стикеры для заданий DBS с доставкой в ПВЗ.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/stickers`"
        ),
    )
    async def get_stickers(
        self,
        data: DBSOrderIdsRequest,
        sticker_type: str = Parameter("png", query="type", description="Формат стикера: `png` или `svg`."),
        width: int = Parameter(58, query="width", description="Ширина стикера в мм."),
        height: int = Parameter(40, query="height", description="Высота стикера в мм."),
    ) -> DBSStickersResponse:
        return await DBSOrdersService().get_stickers(data, sticker_type, width, height)

    @post(
        "/deliver",
        status_code=HTTP_204_NO_CONTENT,
        summary="Перевести сборочные задания в доставку",
        description=(
            "Массово переводит задания DBS в статус `deliver`.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/status/deliver`"
        ),
    )
    async def deliver_orders(self, data: DBSOrderIdsRequest) -> None:
        await DBSOrdersService().deliver_orders(data)

    @post(
        "/receive",
        status_code=HTTP_204_NO_CONTENT,
        summary="Сообщить о получении заказов",
        description=(
            "Переводит задания DBS в статус `receive` — покупатель получил товар.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/status/receive`"
        ),
    )
    async def receive_orders(self, data: DBSReceiveRequest) -> None:
        await DBSOrdersService().receive_orders(data)

    @post(
        "/reject",
        status_code=HTTP_204_NO_CONTENT,
        summary="Сообщить об отказе от заказов",
        description=(
            "Переводит задания DBS в статус `reject` — покупатель отказался от товара.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/status/reject`"
        ),
    )
    async def reject_orders(self, data: DBSRejectRequest) -> None:
        await DBSOrdersService().reject_orders(data)

    # --- Deprecated ---

    @post(
        "/status/v3",
        deprecated=True,
        summary="[DEPRECATED] Получить статусы сборочных заданий",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/status`.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/dbs/orders/status`"
        ),
    )
    async def get_orders_status_deprecated(self, data: DBSOrderIdsRequest) -> DBSOrderStatusResponse:
        return await DBSOrdersService().get_orders_status_deprecated(data)

    @patch(
        "/{order_id:int}/cancel",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Отменить сборочное задание",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/cancel`.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/cancel`"
        ),
    )
    async def cancel_order(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> None:
        await DBSOrdersService().cancel_order(order_id)

    @patch(
        "/{order_id:int}/confirm",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Перевести на сборку",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/confirm`.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/confirm`"
        ),
    )
    async def confirm_order(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> None:
        await DBSOrdersService().confirm_order(order_id)

    @patch(
        "/{order_id:int}/deliver",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Перевести в доставку",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/deliver`.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/deliver`"
        ),
    )
    async def deliver_order(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> None:
        await DBSOrdersService().deliver_order(order_id)

    @patch(
        "/{order_id:int}/receive",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Сообщить о получении заказа",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/receive`.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/receive`"
        ),
    )
    async def receive_order(
        self,
        data: DBSReceiveRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> None:
        await DBSOrdersService().receive_order(order_id, data.model_dump(exclude_none=True))

    @patch(
        "/{order_id:int}/reject",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Сообщить об отказе покупателя",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/reject`.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/reject`"
        ),
    )
    async def reject_order(
        self,
        data: DBSRejectRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> None:
        await DBSOrdersService().reject_order(order_id, data.model_dump(exclude_none=True))
