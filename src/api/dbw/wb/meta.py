"""
Контроллер: DBW / Метаданные сборочных заданий
WB API: marketplace-api.wildberries.ru
Tag: Метаданные DBW (6 endpoints)
"""
from litestar import Controller, delete, get, put
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.dbw.meta import (
    DBWOrderMetaResponse, DBWSetGtinRequest,
    DBWSetImeiRequest, DBWSetSgtinRequest, DBWSetUinRequest,
)
from src.services.dbw.wb.meta import DBWMetaService


class DBWMetaController(Controller):
    path = "/orders"
    tags = ["04. API Wildberries"]

    @get(
        "/{order_id:int}/meta",
        summary="Получить метаданные сборочного задания",
        description=(
            "Возвращает все метаданные сборочного задания DBW: "
            "коды маркировки, IMEI, GTIN, УИН и другие закреплённые данные.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/meta`"
        ),
    )
    async def get_order_meta(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> DBWOrderMetaResponse:
        return await DBWMetaService().get_order_meta(order_id)

    @delete(
        "/{order_id:int}/meta",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить метаданные сборочного задания",
        description=(
            "Удаляет конкретный тип метаданных у задания DBW.\n\n"
            "Допустимые значения `key`: `imei`, `uin`, `gtin`, `sgtin`.\n\n"
            "**WB endpoint:** `DELETE marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/meta`"
        ),
    )
    async def delete_order_meta(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
        key: str = Parameter(
            query="key",
            description="Тип метаданных для удаления: `imei`, `uin`, `gtin`, `sgtin`.",
        ),
    ) -> None:
        await DBWMetaService().delete_order_meta(order_id, key)

    @put(
        "/{order_id:int}/meta/sgtin",
        summary="Закрепить коды маркировки товара",
        description=(
            "Привязывает коды маркировки КИЗ/честный знак к заданию DBW.\n\n"
            "**Отличие от FBS:** передаётся массив кодов `sgtins`, а не один код.\n\n"
            "Допустимая длина каждого кода: 16–135 символов.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/meta/sgtin`"
        ),
    )
    async def set_sgtin(
        self,
        data: DBWSetSgtinRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBWMetaService().set_sgtin(order_id, data)

    @put(
        "/{order_id:int}/meta/uin",
        summary="Закрепить УИН ювелирного изделия",
        description=(
            "Привязывает УИН ювелирного изделия к заданию DBW.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/meta/uin`"
        ),
    )
    async def set_uin(
        self,
        data: DBWSetUinRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBWMetaService().set_uin(order_id, data)

    @put(
        "/{order_id:int}/meta/imei",
        summary="Закрепить IMEI устройства",
        description=(
            "Привязывает IMEI мобильного устройства к заданию DBW.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/meta/imei`"
        ),
    )
    async def set_imei(
        self,
        data: DBWSetImeiRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBWMetaService().set_imei(order_id, data)

    @put(
        "/{order_id:int}/meta/gtin",
        summary="Закрепить GTIN товара",
        description=(
            "Привязывает GTIN товара к заданию DBW.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/dbw/orders/{orderId}/meta/gtin`"
        ),
    )
    async def set_gtin(
        self,
        data: DBWSetGtinRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBWMetaService().set_gtin(order_id, data)
