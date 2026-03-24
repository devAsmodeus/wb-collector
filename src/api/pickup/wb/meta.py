"""
Контроллер: Самовывоз / Метаданные
WB API: marketplace-api.wildberries.ru
Tag: Метаданные Самовывоз (12 endpoints, из них 6 deprecated)
"""
from litestar import Controller, delete, get, post, put
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.pickup.meta import (
    PickupMetaDeleteRequest, PickupMetaInfoRequest,
    PickupSetGtinRequest, PickupSetGtinSingleRequest,
    PickupSetImeiRequest, PickupSetImeiSingleRequest,
    PickupSetSgtinRequest, PickupSetSgtinSingleRequest,
    PickupSetUinRequest, PickupSetUinSingleRequest,
)
from src.services.pickup.wb.meta import PickupMetaService


class PickupMetaController(Controller):
    path = "/orders"
    tags = ["Метаданные Самовывоз"]

    @post(
        "/meta/info",
        summary="Получить метаданные сборочных заданий",
        description=(
            "Возвращает метаданные заданий Самовывоз.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/meta/info`"
        ),
    )
    async def get_meta_info(self, data: PickupMetaInfoRequest) -> dict:
        return await PickupMetaService().get_meta_info(data)

    @post(
        "/meta/delete",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить метаданные сборочных заданий",
        description=(
            "Массово удаляет метаданные указанного типа.\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/meta/delete`"
        ),
    )
    async def delete_meta(self, data: PickupMetaDeleteRequest) -> None:
        await PickupMetaService().delete_meta(data)

    @post(
        "/meta/sgtin",
        summary="Закрепить коды маркировки за сборочными заданиями",
        description=(
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/meta/sgtin`"
        ),
    )
    async def set_sgtin(self, data: PickupSetSgtinRequest) -> dict:
        return await PickupMetaService().set_sgtin(data)

    @post(
        "/meta/uin",
        summary="Закрепить УИН за сборочными заданиями",
        description=(
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/meta/uin`"
        ),
    )
    async def set_uin(self, data: PickupSetUinRequest) -> dict:
        return await PickupMetaService().set_uin(data)

    @post(
        "/meta/imei",
        summary="Закрепить IMEI за сборочными заданиями",
        description=(
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/meta/imei`"
        ),
    )
    async def set_imei(self, data: PickupSetImeiRequest) -> dict:
        return await PickupMetaService().set_imei(data)

    @post(
        "/meta/gtin",
        summary="Закрепить GTIN за сборочными заданиями",
        description=(
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/marketplace/v3/click-collect/orders/meta/gtin`"
        ),
    )
    async def set_gtin(self, data: PickupSetGtinRequest) -> dict:
        return await PickupMetaService().set_gtin(data)

    # --- Deprecated ---

    @get(
        "/{order_id:int}/meta",
        deprecated=True,
        summary="[DEPRECATED] Получить метаданные задания",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/meta/info`.",
    )
    async def get_order_meta(self, order_id: int = Parameter(description="ID задания")) -> dict:
        return await PickupMetaService().get_order_meta(order_id)

    @delete(
        "/{order_id:int}/meta",
        deprecated=True,
        status_code=HTTP_204_NO_CONTENT,
        summary="[DEPRECATED] Удалить метаданные задания",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/meta/delete`.",
    )
    async def delete_order_meta(
        self,
        order_id: int = Parameter(description="ID задания"),
        key: str = Parameter(query="key", description="Тип метаданных: `sgtin`, `uin`, `imei`, `gtin`."),
    ) -> None:
        await PickupMetaService().delete_order_meta(order_id, key)

    @put(
        "/{order_id:int}/meta/sgtin",
        deprecated=True,
        summary="[DEPRECATED] Закрепить код маркировки за заданием",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/meta/sgtin`.",
    )
    async def set_sgtin_single(
        self,
        data: PickupSetSgtinSingleRequest,
        order_id: int = Parameter(description="ID задания"),
    ) -> dict:
        return await PickupMetaService().set_sgtin_single(order_id, data)

    @put(
        "/{order_id:int}/meta/uin",
        deprecated=True,
        summary="[DEPRECATED] Закрепить УИН за заданием",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/meta/uin`.",
    )
    async def set_uin_single(
        self,
        data: PickupSetUinSingleRequest,
        order_id: int = Parameter(description="ID задания"),
    ) -> dict:
        return await PickupMetaService().set_uin_single(order_id, data)

    @put(
        "/{order_id:int}/meta/imei",
        deprecated=True,
        summary="[DEPRECATED] Закрепить IMEI за заданием",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/meta/imei`.",
    )
    async def set_imei_single(
        self,
        data: PickupSetImeiSingleRequest,
        order_id: int = Parameter(description="ID задания"),
    ) -> dict:
        return await PickupMetaService().set_imei_single(order_id, data)

    @put(
        "/{order_id:int}/meta/gtin",
        deprecated=True,
        summary="[DEPRECATED] Закрепить GTIN за заданием",
        description="⚠️ **Устарел.** Используйте `POST /pickup/orders/meta/gtin`.",
    )
    async def set_gtin_single(
        self,
        data: PickupSetGtinSingleRequest,
        order_id: int = Parameter(description="ID задания"),
    ) -> dict:
        return await PickupMetaService().set_gtin_single(order_id, data)
