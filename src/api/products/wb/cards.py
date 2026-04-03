"""
Контроллер: Products / Карточки товаров
WB API: content-api.wildberries.ru
"""
from litestar import Controller, get, post
from litestar.handlers import delete
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

    @post("/", summary="Список карточек товаров",
          description="POST /content/v2/get/cards/list — cursor-based пагинация.")
    async def get_cards(
        self,
        data: CardsListRequest | None = None,
        locale: str = Parameter(default="ru", query="locale"),
    ) -> CardsListResponse:
        return await CardsService().get_cards(request=data, locale=locale)

    @get("/limits", summary="Лимиты карточек товаров",
         description="GET /content/v2/cards/limits")
    async def get_cards_limits(self) -> CardLimitsResponse:
        return await CardsService().get_cards_limits()

    @get("/errors", summary="Карточки с ошибками валидации",
         description="POST /content/v2/cards/error/list")
    async def get_cards_errors(self) -> CardErrorsResponse:
        return await CardsService().get_cards_errors()

    @post("/trash", summary="Карточки в корзине",
          description="POST /content/v2/get/cards/trash")
    async def get_trash_cards(
        self,
        locale: str = Parameter(default="ru", query="locale"),
    ) -> CardsListResponse:
        return await CardsService().get_trash_cards(locale=locale)

    @post("/update", summary="Редактировать карточки ⚠️",
          description="POST /content/v2/cards/update — **изменяет реальные данные**.")
    async def update_cards(self, data: dict) -> dict:
        return await CardsService().update_cards(data.get("cards", []))

    @post("/move", summary="Перенести карточки в другой IMT ⚠️",
          description="POST /content/v2/cards/moveNm")
    async def move_cards(self, data: dict) -> dict:
        return await CardsService().move_cards(
            target_imt=data.get("targetIMT", 0),
            nm_ids=data.get("nmIDs", []),
        )

    @delete("/trash", summary="Удалить карточки в корзину ⚠️",
            description="POST /content/v2/cards/delete/trash", status_code=200)
    async def delete_cards_to_trash(self, data: dict) -> dict:
        return await CardsService().delete_cards_to_trash(data.get("nmIDs", []))

    @post("/recover", summary="Восстановить карточки из корзины ⚠️",
          description="POST /content/v2/cards/recover")
    async def recover_cards(self, data: dict) -> dict:
        return await CardsService().recover_cards(data.get("nmIDs", []))

    @post("/upload", summary="Создать карточки ⚠️",
          description="POST /content/v2/cards/upload")
    async def upload_cards(self, data: dict) -> dict:
        return await CardsService().upload_cards(data.get("cards", []))

    @post("/upload/add", summary="Добавить товары к карточкам ⚠️",
          description="POST /content/v2/cards/upload/add")
    async def upload_add_cards(self, data: dict) -> dict:
        return await CardsService().upload_add_cards(data.get("cards", []))


class BarcodesController(Controller):
    path = "/barcodes"
    tags = ["02. API Wildberries"]

    @post("/", summary="Сгенерировать баркоды",
          description="POST /content/v2/barcodes — генерация EAN-13. Макс. 5000.")
    async def generate_barcodes(
        self,
        count: int = Parameter(query="count", ge=1, le=5000),
    ) -> BarcodesResponse:
        return await CardsService().generate_barcodes(count)
