"""Коллектор: Работа с товарами — Карточки товаров (11 методов).
Хост: content-api.wildberries.ru
"""
from src.collectors.base import WBApiClient
from src.schemas.products.cards import (
    CardsListResponse, CardsListRequest, CardLimitsResponse,
    BarcodesResponse, CardErrorsResponse,
)


class CardsCollector:
    def __init__(self, client: WBApiClient):
        self._client = client

    async def get_cards_list(self, request: CardsListRequest | None = None, locale: str = "ru") -> CardsListResponse:
        """POST /content/v2/get/cards/list — список карточек товаров."""
        body = request.model_dump(exclude_none=True) if request else {}
        data = await self._client.post(
            "/content/v2/get/cards/list", json=body, params={"locale": locale}
        )
        return CardsListResponse.model_validate(data)

    async def get_cards_errors(self, limit: int = 100, ascending: bool = False) -> CardErrorsResponse:
        """POST /content/v2/cards/error/list — карточки с ошибками создания."""
        body = {"cursor": {"limit": limit}, "order": {"ascending": ascending}}
        data = await self._client.post("/content/v2/cards/error/list", json=body)
        return CardErrorsResponse.model_validate(data)

    async def update_cards(self, cards: list[dict]) -> dict:
        """
        POST /content/v2/cards/update — редактирование карточек.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post("/content/v2/cards/update", json=cards)

    async def move_cards(self, target_imt_id: int, nm_ids: list[int]) -> dict:
        """
        POST /content/v2/cards/moveNm — объединение/разъединение карточек.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post(
            "/content/v2/cards/moveNm",
            json={"targetIMT": target_imt_id, "nmIDs": nm_ids},
        )

    async def delete_cards_to_trash(self, nm_ids: list[int]) -> dict:
        """
        POST /content/v2/cards/delete/trash — перенести в корзину.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post("/content/v2/cards/delete/trash", json={"nmIDs": nm_ids})

    async def recover_cards(self, nm_ids: list[int]) -> dict:
        """
        POST /content/v2/cards/recover — восстановить из корзины.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post("/content/v2/cards/recover", json={"nmIDs": nm_ids})

    async def get_trash_cards(self, request: CardsListRequest | None = None, locale: str = "ru") -> CardsListResponse:
        """POST /content/v2/get/cards/trash — карточки в корзине."""
        body = request.model_dump(exclude_none=True) if request else {}
        data = await self._client.post(
            "/content/v2/get/cards/trash", json=body, params={"locale": locale}
        )
        return CardsListResponse.model_validate(data)

    async def get_cards_limits(self) -> CardLimitsResponse:
        """GET /content/v2/cards/limits — лимиты карточек товаров."""
        data = await self._client.get("/content/v2/cards/limits")
        return CardLimitsResponse.model_validate(data)

    async def generate_barcodes(self, count: int) -> BarcodesResponse:
        """POST /content/v2/barcodes — генерация баркодов (макс. 5000)."""
        data = await self._client.post("/content/v2/barcodes", json={"count": count})
        return BarcodesResponse.model_validate(data)

    async def create_cards(self, cards: list[dict]) -> dict:
        """
        POST /content/v2/cards/upload — создание карточек.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post("/content/v2/cards/upload", json=cards)

    async def create_cards_with_attach(self, imt_id: int, cards_to_add: list[dict]) -> dict:
        """
        POST /content/v2/cards/upload/add — создание с присоединением.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post(
            "/content/v2/cards/upload/add",
            json={"imtID": imt_id, "cardsToAdd": cards_to_add},
        )
