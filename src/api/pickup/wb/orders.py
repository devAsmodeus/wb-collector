"""
Контроллер: Самовывоз (Click & Collect) / Сборочные задания
WB API: marketplace-api.wildberries.ru
Tag: Сборочные задания Самовывоз (16 endpoints, из них 6 deprecated)

Самовывоз — покупатель забирает заказ в пункте выдачи продавца.
"""
from litestar import Controller, get, patch, post
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.pickup.orders import (
    PickupOrderIdsRequest, PickupOrderStatusResponse,
    PickupOrdersResponse, PickupReceiveRequest, PickupRejectRequest,
)
from src.services.pickup.wb.orders import PickupOrdersService


class PickupOrdersController(Controller):
    path = "/orders"
    tags = ["Сборочные задания Самовывоз"]

    @get(
        "/new",
        summary="Получить список новых сборочных заданий",
        description=(
            "Возвращает новые задания Самовывоз, ожидающие подтверждения.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/click-collect/orders/new`"
        ),
    )
    async def get_new_orders(self) -> PickupOrdersResponse:
        return await PickupOrdersService().get_new_orders()

    @post(
        "/confirm",
        status_code=HTTP_204_NO_CONTENT,
        summary="Перевести сборочные задания на сборку",
        description=(
            "Массово переводит задания Самовывоз в статус `confirm`.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/status/confirm`"
        ),
    )
    async def confirm_orders(self, data: PickupOrderIdsRequest) -> None:
        await PickupOrdersService().confirm_orders(data)

    @post(
        "/prepare",
        status_code=HTTP_204_NO_CONTENT,
        summary="Подготовить заказы к выдаче",
        description=(
            "Переводит задания в статус `prepare` — заказ готов к выдаче покупателю.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/status/prepare`"
        ),
    )
    async def prepare_orders(self, data: PickupOrderIdsRequest) -> None:
        await PickupOrdersService().prepare_orders(data)

    @post(
        "/client",
        summary="Информация о покупателе",
        description=(
            "Возвращает данные покупателя для заданий Самовывоз.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/click-collect/orders/client`"
        ),
    )
    async def get_client_orders(self, data: PickupOrderIdsRequest) -> dict:
        return await PickupOrdersService().get_client_orders(data)

    @post(
        "/client/identity",
        summary="Идентификация покупателя",
        description=(
            "Возвращает данные для идентификации покупателя при выдаче заказа.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/click-collect/orders/client/identity`"
        ),
    )
    async def get_client_identity(self, data: PickupOrderIdsRequest) -> dict:
        return await PickupOrdersService().get_client_identity(data)

    @post(
        "/receive",
        status_code=HTTP_204_NO_CONTENT,
        summary="Сообщить о выдаче заказов покупателю",
        description=(
            "Переводит задания в статус `receive` — товар выдан покупателю.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/status/receive`"
        ),
    )
    async def receive_orders(self, data: PickupReceiveRequest) -> None:
        await PickupOrdersService().receive_orders(data)

    @post(
        "/reject",
        status_code=HTTP_204_NO_CONTENT,
        summary="Сообщить об отказе от заказов",
        description=(
            "Переводит задания в статус `reject` — покупатель отказался от товара.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/status/reject`"
        ),
    )
    async def reject_orders(self, data: PickupRejectRequest) -> None:
        await PickupOrdersService().reject_orders(data)

    @post(
        "/status",
        summary="Получить статусы сборочных заданий",
        description=(
            "Возвращает статусы заданий Самовывоз.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/status/info`"
        ),
    )
    async def get_orders_status(self, data: PickupOrderIdsRequest) -> PickupOrderStatusResponse:
        return await PickupOrdersService().get_orders_status(data)

    @get(
        "/",
        summary="Получить информацию о завершённых сборочных заданиях",
        description=(
            "Возвращает завершённые задания Самовывоз за период.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/click-collect/orders`"
        ),
    )
    async def get_orders(
        self,
        date_from: int | None = Parameter(None, query="date_from", description="Начало периода, Unix timestamp (сек)."),
        date_to: int | None = Parameter(None, query="date_to", description="Конец периода, Unix timestamp (сек)."),
    ) -> PickupOrdersResponse:
        return await PickupOrdersService().get_orders(date_from=date_from, date_to=date_to)

    @post(
        "/cancel",
        status_code=HTTP_204_NO_CONTENT,
        summary="Отменить сборочные задания",
        description=(
            "Массово отменяет задания Самовывоз.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/status/cancel`"
        ),
    )
    async def cancel_orders(self, data: PickupOrderIdsRequest) -> None:
        await PickupOrdersService().cancel_orders(data)

    # --- Deprecated ---

    @patch(
        "/{order_id:int}/confirm",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Перевести на сборку",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/confirm`.",
    )
    async def confirm_order(self, order_id: int = Parameter(description="ID задания")) -> None:
        await PickupOrdersService().confirm_order(order_id)

    @patch(
        "/{order_id:int}/prepare",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Подготовить к выдаче",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/prepare`.",
    )
    async def prepare_order(self, order_id: int = Parameter(description="ID задания")) -> None:
        await PickupOrdersService().prepare_order(order_id)

    @patch(
        "/{order_id:int}/receive",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Сообщить о выдаче заказа",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/receive`.",
    )
    async def receive_order(self, order_id: int = Parameter(description="ID задания")) -> None:
        await PickupOrdersService().receive_order(order_id)

    @patch(
        "/{order_id:int}/reject",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Сообщить об отказе покупателя",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/reject`.",
    )
    async def reject_order(
        self,
        data: PickupRejectRequest,
        order_id: int = Parameter(description="ID задания"),
    ) -> None:
        await PickupOrdersService().reject_order(order_id, data.model_dump(exclude_none=True))

    @post(
        "/status/v3",
        deprecated=True,
        summary="[DEPRECATED] Получить статусы сборочных заданий",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/status`.",
    )
    async def get_orders_status_deprecated(self, data: PickupOrderIdsRequest) -> PickupOrderStatusResponse:
        return await PickupOrdersService().get_orders_status_deprecated(data)

    @patch(
        "/{order_id:int}/cancel",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Отменить сборочное задание",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/cancel`.",
    )
    async def cancel_order(self, order_id: int = Parameter(description="ID задания")) -> None:
        await PickupOrdersService().cancel_order(order_id)
