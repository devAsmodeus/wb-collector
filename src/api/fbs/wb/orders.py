"""
Контроллер: FBS / Сборочные задания
WB API: marketplace-api.wildberries.ru
Tag: Сборочные задания FBS (9 endpoints)
"""
from litestar import Controller, get, patch, post
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.fbs.orders import (
    OrderStatusRequest, OrderStatusResponse,
    OrdersResponse,
    StickersRequest, StickersResponse,
    ClientOrdersRequest,
)
from src.services.fbs.wb.orders import OrdersService


class OrdersController(Controller):
    path = "/orders"
    tags = ["Сборочные задания FBS"]

    @get(
        "/new",
        summary="Получить список новых сборочных заданий",
        description=(
            "Возвращает сборочные задания в статусе `waiting` — ожидающие сборки продавцом.\n\n"
            "Рекомендуется опрашивать каждые 5–15 минут.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/orders/new`"
        ),
    )
    async def get_new_orders(self) -> OrdersResponse:
        return await OrdersService().get_new_orders()

    @get(
        "/",
        summary="Получить информацию о сборочных заданиях",
        description=(
            "Возвращает сборочные задания за указанный период с пагинацией. "
            "Включает задания во всех статусах.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/orders`"
        ),
    )
    async def get_orders(
        self,
        date_from: int | None = Parameter(
            None, query="date_from",
            description="Начало периода, Unix timestamp (сек). По умолчанию — последние 30 дней.",
        ),
        date_to: int | None = Parameter(
            None, query="date_to",
            description="Конец периода, Unix timestamp (сек). По умолчанию — текущий момент.",
        ),
        limit: int = Parameter(
            1000, query="limit", ge=1, le=1000,
            description="Количество заданий в ответе (1–1000). По умолчанию: 1000.",
        ),
        offset: int = Parameter(
            0, query="offset", ge=0,
            description="Смещение для пагинации. По умолчанию: 0.",
        ),
    ) -> OrdersResponse:
        return await OrdersService().get_orders(date_from=date_from, date_to=date_to, limit=limit, offset=offset)

    @post(
        "/status",
        summary="Получить статусы сборочных заданий",
        description=(
            "Возвращает `supplierStatus` (статус продавца) и `wbStatus` (внутренний статус WB) "
            "для каждого задания.\n\nМаксимум **1000** заданий за запрос.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/orders/status`"
        ),
    )
    async def get_orders_status(self, data: OrderStatusRequest) -> OrderStatusResponse:
        return await OrdersService().get_orders_status(data)

    @get(
        "/reshipment",
        summary="Получить все сборочные задания для повторной отгрузки",
        description=(
            "Возвращает задания, которые нужно отгрузить повторно (товар утерян или не получен).\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/supplies/orders/reshipment`"
        ),
    )
    async def get_reshipment_orders(self) -> OrdersResponse:
        return await OrdersService().get_reshipment_orders()

    @patch(
        "/{order_id:int}/cancel",
        status_code=HTTP_204_NO_CONTENT,
        summary="Отменить сборочное задание",
        description=(
            "Отменяет задание в статусах `waiting` или `confirm`.\n\n"
            "**WB endpoint:** `PATCH marketplace-api.wildberries.ru/api/v3/orders/{orderId}/cancel`"
        ),
    )
    async def cancel_order(
        self,
        order_id: int = Parameter(description="ID сборочного задания для отмены"),
    ) -> None:
        await OrdersService().cancel_order(order_id)

    @post(
        "/stickers",
        summary="Получить стикеры сборочных заданий",
        description=(
            "Возвращает стикеры (этикетки) для наклейки на товары.\n\n"
            "**Форматы:** `png` (растр) или `svg` (вектор).\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/orders/stickers`"
        ),
    )
    async def get_stickers(
        self,
        data: StickersRequest,
        sticker_type: str = Parameter(
            "png", query="type",
            description="Формат стикера: `png` (по умолчанию) или `svg`.",
        ),
        width: int = Parameter(58, query="width", description="Ширина стикера в мм. По умолчанию: 58."),
        height: int = Parameter(40, query="height", description="Высота стикера в мм. По умолчанию: 40."),
    ) -> StickersResponse:
        return await OrdersService().get_stickers(data, sticker_type, width, height)

    @post(
        "/stickers/cross-border",
        summary="Получить стикеры сборочных заданий кроссбордера",
        description=(
            "Возвращает стикеры для заданий международной доставки (кроссбордер).\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/orders/stickers/cross-border`"
        ),
    )
    async def get_crossborder_stickers(self, data: StickersRequest) -> StickersResponse:
        return await OrdersService().get_crossborder_stickers(data)

    @post(
        "/status/history",
        summary="История статусов для сборочных заданий кроссбордера",
        description=(
            "Возвращает историю изменения статусов для кроссбордер заданий.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/orders/status/history`"
        ),
    )
    async def get_status_history(self, data: OrderStatusRequest) -> dict:
        return await OrdersService().get_status_history(data)

    @post(
        "/client",
        summary="Заказы с информацией по клиенту",
        description=(
            "Возвращает задания с дополнительными данными о покупателе.\n\n"
            "⚠️ Данные клиента доступны только для заданий в статусе `confirm` и выше.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/orders/client`"
        ),
    )
    async def get_client_orders(self, data: ClientOrdersRequest) -> dict:
        return await OrdersService().get_client_orders(data.orders)
