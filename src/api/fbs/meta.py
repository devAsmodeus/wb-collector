"""
Контроллер: FBS / Метаданные сборочных заданий
WB API: marketplace-api.wildberries.ru
Tag: Метаданные FBS (8 endpoints)
"""
from litestar import Controller, delete, post, put
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.fbs.orders import (
    OrderMetaRequest, OrderMetaResponse,
    SetCustomsRequest, SetExpirationRequest,
    SetGtinRequest, SetImeiRequest, SetSgtinRequest, SetUinRequest,
)
from src.services.fbs.orders import OrdersService


class MetaController(Controller):
    path = "/orders"
    tags = ["Метаданные FBS"]

    @post(
        "/meta",
        summary="Получить метаданные сборочных заданий",
        description=(
            "Возвращает метаданные (коды маркировки, IMEI, GTIN, срок годности и др.) "
            "для указанных сборочных заданий.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/orders/meta`"
        ),
    )
    async def get_orders_meta(self, data: OrderMetaRequest) -> OrderMetaResponse:
        return await OrdersService().get_orders_meta(data)

    @delete(
        "/{order_id:int}/meta",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить метаданные сборочного задания",
        description=(
            "Удаляет конкретный тип метаданных у сборочного задания.\n\n"
            "Типы: `sgtin`, `uin`, `imei`, `gtin`, `expirationDate`, `customsDeclarationNumber`.\n\n"
            "**WB endpoint:** `DELETE marketplace-api.wildberries.ru/api/v3/orders/{orderId}/meta`"
        ),
    )
    async def delete_order_meta(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
        key: str = Parameter(
            query="key",
            description="Тип метаданных для удаления: `sgtin`, `uin`, `imei`, `gtin`, `expirationDate`, `customsDeclarationNumber`.",
        ),
    ) -> None:
        await OrdersService().delete_order_meta(order_id, key)

    @put(
        "/{order_id:int}/meta/sgtin",
        summary="Закрепить за сборочным заданием код маркировки товара",
        description=(
            "Привязывает SGTIN (КИЗ / честный знак) к сборочному заданию.\n\n"
            "Обязательно для обуви, одежды, парфюма, шин и др. товаров обязательной маркировки.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/orders/{orderId}/meta/sgtin`"
        ),
    )
    async def set_order_sgtin(
        self,
        data: SetSgtinRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await OrdersService().set_order_sgtin(order_id, data.sgtin)

    @put(
        "/{order_id:int}/meta/uin",
        summary="Закрепить за сборочным заданием УИН",
        description=(
            "Привязывает УИН (уникальный идентификационный номер) ювелирного изделия.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/orders/{orderId}/meta/uin`"
        ),
    )
    async def set_order_uin(
        self,
        data: SetUinRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await OrdersService().set_order_uin(order_id, data.uin)

    @put(
        "/{order_id:int}/meta/imei",
        summary="Закрепить за сборочным заданием IMEI",
        description=(
            "Привязывает IMEI мобильного устройства к сборочному заданию.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/orders/{orderId}/meta/imei`"
        ),
    )
    async def set_order_imei(
        self,
        data: SetImeiRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await OrdersService().set_order_imei(order_id, data.imei)

    @put(
        "/{order_id:int}/meta/gtin",
        summary="Закрепить за сборочным заданием GTIN",
        description=(
            "Привязывает GTIN (глобальный идентификатор торговой единицы) к сборочному заданию.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/orders/{orderId}/meta/gtin`"
        ),
    )
    async def set_order_gtin(
        self,
        data: SetGtinRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await OrdersService().set_order_gtin(order_id, data.gtin)

    @put(
        "/{order_id:int}/meta/expiration",
        summary="Закрепить за сборочным заданием срок годности товара",
        description=(
            "Привязывает срок годности к сборочному заданию.\n\n"
            "Обязательно для продуктов питания, косметики и аналогичных товаров.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/orders/{orderId}/meta/expiration`"
        ),
    )
    async def set_order_expiration(
        self,
        data: SetExpirationRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await OrdersService().set_order_expiration(order_id, data.expirationDate)

    @put(
        "/{order_id:int}/meta/customs-declaration",
        summary="Закрепить за сборочным заданием номер ГТД",
        description=(
            "Привязывает номер грузовой таможенной декларации (ГТД) для импортных товаров.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/marketplace/v3/orders/{orderId}/meta/customs-declaration`"
        ),
    )
    async def set_order_customs(
        self,
        data: SetCustomsRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await OrdersService().set_order_customs(order_id, data.customsDeclarationNumber)
