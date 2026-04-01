"""
Контроллер: Products / Карточки товаров
WB API: content-api.wildberries.ru

Управление карточками товаров: получение списка, лимиты,
ошибки валидации, корзина и генерация баркодов.
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.products.cards import (
    BarcodesResponse,
    CardErrorsResponse,
    CardLimitsResponse,
    CardsListRequest,
    CardsListResponse,
)
from src.services.products.wb.cards import CardsService


class CardsController(Controller):
    path = "/cards"
    tags = ["02. API Wildberries"]

    @post(
        "/",
        summary="Список карточек товаров",
        description=(
            "Возвращает карточки товаров с cursor-based пагинацией.\n\n"
            "**Первый запрос:** передайте только `cursor.limit`.\n\n"
            "**Следующие страницы:** передайте `cursor.updatedAt` и `cursor.nmID` "
            "из предыдущего ответа.\n\n"
            "**Фильтры** (`settings.filter`):\n"
            "- `textSearch` — поиск по названию / артикулу\n"
            "- `tagIDs` — фильтр по тегам\n"
            "- `objectIDs` — фильтр по предметам\n"
            "- `brands` — фильтр по брендам\n\n"
            "**WB endpoint:** `POST content-api.wildberries.ru/api/v2/get/cards/list`"
        ),
    )
    async def get_cards(
        self,
        data: CardsListRequest | None = None,
        locale: str = Parameter(
            "ru",
            query="locale",
            description="Язык характеристик в ответе: `ru` (по умолчанию), `en`, `zh`.",
        ),
    ) -> CardsListResponse:
        return await CardsService().get_cards(request=data, locale=locale)

    @get(
        "/limits",
        summary="Лимиты карточек товаров",
        description=(
            "Возвращает информацию о лимитах на создание карточек:\n\n"
            "- `freeLimitBase` — базовый бесплатный лимит\n"
            "- `paidLimitBase` — платный лимит\n"
            "- `used` — уже использовано\n"
            "- `freeToUse` — доступно прямо сейчас\n\n"
            "**WB endpoint:** `GET content-api.wildberries.ru/api/v2/cards/limits`"
        ),
    )
    async def get_cards_limits(self) -> CardLimitsResponse:
        return await CardsService().get_cards_limits()

    @get(
        "/errors",
        summary="Карточки с ошибками валидации",
        description=(
            "Возвращает карточки, которые не прошли валидацию WB при создании или редактировании.\n\n"
            "Ошибки сгруппированы по артикулам продавца (`vendorCodes`) и батчам загрузки.\n\n"
            "Используйте для диагностики проблем при массовой загрузке товаров.\n\n"
            "**WB endpoint:** `GET content-api.wildberries.ru/api/v2/cards/error/list`"
        ),
    )
    async def get_cards_errors(self) -> CardErrorsResponse:
        return await CardsService().get_cards_errors()

    @post(
        "/trash",
        summary="Карточки в корзине",
        description=(
            "Возвращает карточки товаров, перемещённые в корзину (удалённые).\n\n"
            "Карточки из корзины можно восстановить в течение 30 дней.\n\n"
            "Принимает те же параметры фильтрации, что и `POST /cards`.\n\n"
            "**WB endpoint:** `POST content-api.wildberries.ru/api/v2/get/cards/trash`"
        ),
    )
    async def get_trash_cards(
        self,
        locale: str = Parameter(
            "ru",
            query="locale",
            description="Язык характеристик: `ru` (по умолчанию), `en`, `zh`.",
        ),
    ) -> CardsListResponse:
        return await CardsService().get_trash_cards(locale=locale)


class BarcodesController(Controller):
    path = "/barcodes"
    tags = ["02. API Wildberries"]

    @post(
        "/",
        summary="Сгенерировать баркоды",
        description=(
            "Генерирует уникальные баркоды (EAN-13) для привязки к размерам карточек.\n\n"
            "Сгенерированные баркоды нужно записать в поле `skus` нужного размера карточки.\n\n"
            "Максимум **5000 баркодов** за один запрос.\n\n"
            "**WB endpoint:** `POST content-api.wildberries.ru/api/v2/barcodes`"
        ),
    )
    async def generate_barcodes(
        self,
        count: int = Parameter(
            query="count",
            ge=1,
            le=5000,
            description="Количество баркодов для генерации. Диапазон: 1–5000.",
        ),
    ) -> BarcodesResponse:
        return await CardsService().generate_barcodes(count)
