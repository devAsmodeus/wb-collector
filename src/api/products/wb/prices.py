"""
Контроллер: Products / Цены и скидки
WB API: discounts-prices-api.wildberries.ru

Получение актуальных цен, скидок, истории загрузок и карантина.
Изменение цен происходит через отдельные batch-задачи (uploadID).
"""
from litestar import Controller, get
from litestar.params import Parameter

from src.schemas.products.prices import (
    GoodsListResponse,
    PriceHistoryResponse,
    QuarantineResponse,
    UploadGoodsResponse,
)
from src.services.products.wb.prices import PricesService


class PricesController(Controller):
    path = "/prices"
    tags = ["Products — Цены"]

    @get(
        "/goods",
        summary="Товары с ценами и скидками",
        description=(
            "Возвращает список всех товаров продавца с текущими ценами и скидками.\n\n"
            "**Цены хранятся в копейках × 100** — делите на 100 для отображения:\n"
            "`300000 → 3000 ₽`\n\n"
            "Поддерживает пагинацию через `limit` / `offset`.\n\n"
            "**WB endpoint:** `GET discounts-prices-api.wildberries.ru/api/v2/list/goods/filter`"
        ),
    )
    async def get_goods(
        self,
        limit: int = Parameter(
            100,
            query="limit",
            ge=1,
            le=1000,
            description="Количество товаров в ответе. Диапазон: 1–1000. По умолчанию: 100.",
        ),
        offset: int = Parameter(
            0,
            query="offset",
            ge=0,
            description="Смещение для пагинации. По умолчанию: 0.",
        ),
    ) -> GoodsListResponse:
        return await PricesService().get_goods(limit=limit, offset=offset)

    @get(
        "/goods/sizes",
        summary="Цены по размерам конкретного товара",
        description=(
            "Возвращает детализацию цен по каждому размеру (chrtID) указанного товара.\n\n"
            "Используется когда у товара включён `editableSizePrice=true` "
            "(разные цены для разных размеров).\n\n"
            "**WB endpoint:** `GET discounts-prices-api.wildberries.ru/api/v2/list/goods/size/nm`"
        ),
    )
    async def get_goods_sizes(
        self,
        nm_id: int = Parameter(
            query="nm_id",
            description="Артикул WB (nmID) товара, по которому нужна детализация цен.",
        ),
    ) -> GoodsListResponse:
        return await PricesService().get_goods_sizes(nm_id)

    @get(
        "/goods/quarantine",
        summary="Товары на карантине цен",
        description=(
            "Возвращает товары, заблокированные WB из-за подозрительного изменения цены.\n\n"
            "**Карантин срабатывает когда:**\n"
            "- Цена выросла более чем на 50% — `priceIncreased`\n"
            "- Цена снизилась более чем на 50% — `priceDecreased`\n\n"
            "Пока товар на карантине, изменения цены не применяются. "
            "Нужно подтвердить изменение в кабинете WB.\n\n"
            "**WB endpoint:** `GET discounts-prices-api.wildberries.ru/api/v2/list/goods/quarantine`"
        ),
    )
    async def get_quarantine(
        self,
        limit: int = Parameter(
            100,
            query="limit",
            ge=1,
            le=1000,
            description="Количество товаров в ответе. По умолчанию: 100.",
        ),
        offset: int = Parameter(
            0,
            query="offset",
            ge=0,
            description="Смещение для пагинации. По умолчанию: 0.",
        ),
    ) -> QuarantineResponse:
        return await PricesService().get_quarantine(limit=limit, offset=offset)

    @get(
        "/history",
        summary="История загрузок цен",
        description=(
            "Возвращает список задач (батчей) обновления цен с их статусами.\n\n"
            "Каждая загрузка получает `uploadID` — по нему можно проверить "
            "какие конкретно товары были обновлены через `/prices/history/goods`.\n\n"
            "**Статусы:** `1` — в обработке, `2` — выполнена, `3` — ошибка.\n\n"
            "**WB endpoint:** `GET discounts-prices-api.wildberries.ru/api/v2/history/tasks`"
        ),
    )
    async def get_upload_history(
        self,
        limit: int = Parameter(
            100,
            query="limit",
            ge=1,
            le=1000,
            description="Количество задач в ответе. По умолчанию: 100.",
        ),
        offset: int = Parameter(
            0,
            query="offset",
            ge=0,
            description="Смещение для пагинации. По умолчанию: 0.",
        ),
    ) -> PriceHistoryResponse:
        return await PricesService().get_upload_history(limit=limit, offset=offset)

    @get(
        "/history/goods",
        summary="Товары конкретной загрузки цен",
        description=(
            "Возвращает список товаров, входивших в конкретную задачу обновления цен.\n\n"
            "Для каждого товара указан статус обработки (`success` / `error`) "
            "и текст ошибки если она возникла.\n\n"
            "**Workflow:** `GET /prices/history` → получить `uploadID` → "
            "`GET /prices/history/goods?upload_id={uploadID}`\n\n"
            "**WB endpoint:** `GET discounts-prices-api.wildberries.ru/api/v2/history/goods`"
        ),
    )
    async def get_upload_goods(
        self,
        upload_id: int = Parameter(
            query="upload_id",
            description="ID задачи загрузки цен (uploadID из `/prices/history`).",
        ),
    ) -> UploadGoodsResponse:
        return await PricesService().get_upload_goods(upload_id)

    @get(
        "/buffer",
        summary="Задачи в буфере (отложенные изменения цен)",
        description=(
            "Возвращает задачи обновления цен, находящиеся в буфере — "
            "ещё не применённые изменения.\n\n"
            "Буфер используется когда изменения запланированы на будущую дату "
            "(`activationDate` в будущем).\n\n"
            "**WB endpoint:** `GET discounts-prices-api.wildberries.ru/api/v2/buffer/tasks`"
        ),
    )
    async def get_buffer_tasks(
        self,
        limit: int = Parameter(
            100,
            query="limit",
            ge=1,
            le=1000,
            description="Количество задач в ответе. По умолчанию: 100.",
        ),
        offset: int = Parameter(
            0,
            query="offset",
            ge=0,
            description="Смещение для пагинации. По умолчанию: 0.",
        ),
    ) -> PriceHistoryResponse:
        return await PricesService().get_buffer_tasks(limit=limit, offset=offset)

    @get(
        "/buffer/goods",
        summary="Товары из буфера по ID задачи",
        description=(
            "Возвращает список товаров конкретной задачи из буфера отложенных изменений.\n\n"
            "**Workflow:** `GET /prices/buffer` → получить `uploadID` → "
            "`GET /prices/buffer/goods?upload_id={uploadID}`\n\n"
            "**WB endpoint:** `GET discounts-prices-api.wildberries.ru/api/v2/buffer/goods`"
        ),
    )
    async def get_buffer_goods(
        self,
        upload_id: int = Parameter(
            query="upload_id",
            description="ID задачи из буфера (uploadID из `/prices/buffer`).",
        ),
    ) -> UploadGoodsResponse:
        return await PricesService().get_buffer_goods(upload_id)
