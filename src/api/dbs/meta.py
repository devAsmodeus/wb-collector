"""
Контроллер: DBS / Метаданные сборочных заданий
WB API: marketplace-api.wildberries.ru
Tag: Метаданные DBS (13 endpoints, из них 6 deprecated)
"""
from litestar import Controller, delete, get, post, put
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.dbs.meta import (
    DBSMetaDeleteRequest, DBSMetaInfoRequest,
    DBSSetCustomsRequest, DBSSetGtinRequest,
    DBSSetGtinSingleRequest, DBSSetImeiRequest,
    DBSSetImeiSingleRequest, DBSSetSgtinRequest,
    DBSSetSgtinSingleRequest, DBSSetUinRequest,
    DBSSetUinSingleRequest,
)
from src.services.dbs.meta import DBSMetaService


class DBSMetaController(Controller):
    path = "/orders"
    tags = ["Метаданные DBS"]

    @post(
        "/meta/info",
        summary="Получить метаданные сборочных заданий",
        description=(
            "Возвращает все метаданные (коды маркировки, IMEI, GTIN и др.) "
            "для указанных заданий DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/meta/info`"
        ),
    )
    async def get_meta_info(self, data: DBSMetaInfoRequest) -> dict:
        return await DBSMetaService().get_meta_info(data)

    @post(
        "/meta/delete",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить метаданные сборочных заданий",
        description=(
            "Массово удаляет метаданные указанного типа у заданий DBS.\n\n"
            "Допустимые значения `key`: `sgtin`, `uin`, `imei`, `gtin`, `customsDeclarationNumber`.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/meta/delete`"
        ),
    )
    async def delete_meta(self, data: DBSMetaDeleteRequest) -> None:
        await DBSMetaService().delete_meta(data)

    @post(
        "/meta/sgtin",
        summary="Закрепить коды маркировки за сборочными заданиями",
        description=(
            "Массово привязывает коды маркировки КИЗ/честный знак к заданиям DBS.\n\n"
            "Каждый элемент содержит `orderId` и массив `sgtins` (16–135 символов каждый).\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/meta/sgtin`"
        ),
    )
    async def set_sgtin(self, data: DBSSetSgtinRequest) -> dict:
        return await DBSMetaService().set_sgtin(data)

    @post(
        "/meta/uin",
        summary="Закрепить УИН за сборочными заданиями",
        description=(
            "Массово привязывает УИН ювелирных изделий к заданиям DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/meta/uin`"
        ),
    )
    async def set_uin(self, data: DBSSetUinRequest) -> dict:
        return await DBSMetaService().set_uin(data)

    @post(
        "/meta/imei",
        summary="Закрепить IMEI за сборочными заданиями",
        description=(
            "Массово привязывает IMEI мобильных устройств к заданиям DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/meta/imei`"
        ),
    )
    async def set_imei(self, data: DBSSetImeiRequest) -> dict:
        return await DBSMetaService().set_imei(data)

    @post(
        "/meta/gtin",
        summary="Закрепить GTIN за сборочными заданиями",
        description=(
            "Массово привязывает GTIN товаров к заданиям DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/meta/gtin`"
        ),
    )
    async def set_gtin(self, data: DBSSetGtinRequest) -> dict:
        return await DBSMetaService().set_gtin(data)

    @post(
        "/meta/customs-declaration",
        summary="Закрепить номер ГТД за сборочными заданиями",
        description=(
            "Массово привязывает номера грузовых таможенных деклараций к заданиям DBS.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/dbs/orders/meta/customs-declaration`"
        ),
    )
    async def set_customs(self, data: DBSSetCustomsRequest) -> dict:
        return await DBSMetaService().set_customs(data)

    # --- Deprecated ---

    @get(
        "/{order_id:int}/meta",
        deprecated=True,
        summary="[DEPRECATED] Получить метаданные сборочного задания",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/meta/info`.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/meta`"
        ),
    )
    async def get_order_meta(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBSMetaService().get_order_meta(order_id)

    @delete(
        "/{order_id:int}/meta",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Удалить метаданные сборочного задания",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/meta/delete`.\n\n"
            "**WB endpoint:** `DELETE marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/meta`"
        ),
    )
    async def delete_order_meta(
        self,
        order_id: int = Parameter(description="ID сборочного задания"),
        key: str = Parameter(query="key", description="Тип метаданных: `sgtin`, `uin`, `imei`, `gtin`."),
    ) -> None:
        await DBSMetaService().delete_order_meta(order_id, key)

    @put(
        "/{order_id:int}/meta/sgtin",
        deprecated=True,
        summary="[DEPRECATED] Закрепить код маркировки за заданием",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/meta/sgtin`.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/meta/sgtin`"
        ),
    )
    async def set_sgtin_single(
        self,
        data: DBSSetSgtinSingleRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBSMetaService().set_sgtin_single(order_id, data)

    @put(
        "/{order_id:int}/meta/uin",
        deprecated=True,
        summary="[DEPRECATED] Закрепить УИН за заданием",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/meta/uin`.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/meta/uin`"
        ),
    )
    async def set_uin_single(
        self,
        data: DBSSetUinSingleRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBSMetaService().set_uin_single(order_id, data)

    @put(
        "/{order_id:int}/meta/imei",
        deprecated=True,
        summary="[DEPRECATED] Закрепить IMEI за заданием",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/meta/imei`.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/meta/imei`"
        ),
    )
    async def set_imei_single(
        self,
        data: DBSSetImeiSingleRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBSMetaService().set_imei_single(order_id, data)

    @put(
        "/{order_id:int}/meta/gtin",
        deprecated=True,
        summary="[DEPRECATED] Закрепить GTIN за заданием",
        description=(
            "⚠️ **Устарел.** Используйте `POST /dbs/orders/meta/gtin`.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/dbs/orders/{orderId}/meta/gtin`"
        ),
    )
    async def set_gtin_single(
        self,
        data: DBSSetGtinSingleRequest,
        order_id: int = Parameter(description="ID сборочного задания"),
    ) -> dict:
        return await DBSMetaService().set_gtin_single(order_id, data)
