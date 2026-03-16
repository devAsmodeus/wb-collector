"""
Коллектор: 02-products (49 методов)
Хосты:
  content-api.wildberries.ru          — /content/* (справочники, ярлыки, карточки, медиа)
  discounts-prices-api.wildberries.ru — /api/v2/*  (цены, скидки, история)
  marketplace-api.wildberries.ru      — /api/v3/*  (остатки, склады)
"""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.products import (
    ParentCategoriesResponse, SubjectsResponse, SubjectCharcsResponse,
    TnvedResponse, BrandsResponse, TagsResponse,
    CardsListResponse, CardsListRequest, CardLimitsResponse, BarcodesResponse,
    CardErrorsResponse, GoodsListResponse, PriceHistoryResponse,
    WBOfficesResponse, SellerWarehousesResponse, SellerWarehouse,
    DBWContactsResponse,
)


class ProductsCollector:
    def __init__(self):
        self._content = WBApiClient(base_url=settings.WB_CONTENT_URL)
        self._prices = WBApiClient(base_url=settings.WB_PRICES_URL)
        self._market = WBApiClient(base_url=settings.WB_MARKETPLACE_URL)

    async def __aenter__(self):
        await self._content.__aenter__()
        await self._prices.__aenter__()
        await self._market.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._content.__aexit__(*args)
        await self._prices.__aexit__(*args)
        await self._market.__aexit__(*args)

    # ─── Справочники ─────────────────────────────────────────────────────────

    async def get_parent_categories(self, locale: str = "ru") -> ParentCategoriesResponse:
        """GET /content/v2/object/parent/all — родительские категории."""
        data = await self._content.get("/content/v2/object/parent/all", params={"locale": locale})
        return ParentCategoriesResponse.model_validate(data)

    async def get_subjects(
        self,
        locale: str = "ru",
        name: str | None = None,
        limit: int = 1000,
        offset: int = 0,
        parent_id: int | None = None,
    ) -> SubjectsResponse:
        """GET /content/v2/object/all — список предметов."""
        params = {"locale": locale, "limit": limit, "offset": offset}
        if name:
            params["name"] = name
        if parent_id is not None:
            params["parentID"] = parent_id
        data = await self._content.get("/content/v2/object/all", params=params)
        return SubjectsResponse.model_validate(data)

    async def get_subject_charcs(self, subject_id: int, locale: str = "ru") -> SubjectCharcsResponse:
        """GET /content/v2/object/charcs/{subjectId} — характеристики предмета."""
        data = await self._content.get(
            f"/content/v2/object/charcs/{subject_id}", params={"locale": locale}
        )
        return SubjectCharcsResponse.model_validate(data)

    async def get_colors(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/colors — цвета."""
        return await self._content.get("/content/v2/directory/colors", params={"locale": locale})

    async def get_kinds(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/kinds — пол."""
        return await self._content.get("/content/v2/directory/kinds", params={"locale": locale})

    async def get_countries(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/countries — страны производства."""
        return await self._content.get("/content/v2/directory/countries", params={"locale": locale})

    async def get_seasons(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/seasons — сезоны."""
        return await self._content.get("/content/v2/directory/seasons", params={"locale": locale})

    async def get_vat_rates(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/vat — ставки НДС."""
        return await self._content.get("/content/v2/directory/vat", params={"locale": locale})

    async def get_tnved(self, subject_id: int, search: int | None = None, locale: str = "ru") -> TnvedResponse:
        """GET /content/v2/directory/tnved — ТНВЭД-коды предмета."""
        params = {"subjectID": subject_id, "locale": locale}
        if search is not None:
            params["search"] = search
        data = await self._content.get("/content/v2/directory/tnved", params=params)
        return TnvedResponse.model_validate(data)

    async def get_brands(self, subject_id: int, next_cursor: int | None = None) -> BrandsResponse:
        """GET /api/content/v1/brands — бренды предмета."""
        params = {"subjectId": subject_id}
        if next_cursor is not None:
            params["next"] = next_cursor
        data = await self._content.get("/api/content/v1/brands", params=params)
        return BrandsResponse.model_validate(data)

    # ─── Ярлыки ──────────────────────────────────────────────────────────────

    async def get_tags(self) -> TagsResponse:
        """GET /content/v2/tags — список ярлыков."""
        data = await self._content.get("/content/v2/tags")
        return TagsResponse.model_validate(data)

    async def create_tag(self, name: str, color: str) -> dict:
        """POST /content/v2/tag — создать ярлык."""
        return await self._content.post("/content/v2/tag", json={"name": name, "color": color})

    async def update_tag(self, tag_id: int, name: str | None = None, color: str | None = None) -> dict:
        """PATCH /content/v2/tag/{id} — изменить ярлык."""
        body = {}
        if name is not None:
            body["name"] = name
        if color is not None:
            body["color"] = color
        return await self._content.patch(f"/content/v2/tag/{tag_id}", json=body)

    async def delete_tag(self, tag_id: int) -> dict:
        """DELETE /content/v2/tag/{id} — удалить ярлык."""
        return await self._content.delete(f"/content/v2/tag/{tag_id}")

    async def link_tags_to_card(self, nm_id: int, tag_ids: list[int]) -> dict:
        """POST /content/v2/tag/nomenclature/link — привязать ярлыки к карточке."""
        return await self._content.post(
            "/content/v2/tag/nomenclature/link",
            json={"nmID": nm_id, "tagsIDs": tag_ids},
        )

    # ─── Карточки товаров ────────────────────────────────────────────────────

    async def get_cards_list(self, request: CardsListRequest | None = None, locale: str = "ru") -> CardsListResponse:
        """POST /content/v2/get/cards/list — список карточек товаров."""
        body = request.model_dump(exclude_none=True) if request else {}
        data = await self._content.post(
            "/content/v2/get/cards/list",
            json=body,
            params={"locale": locale},
        )
        return CardsListResponse.model_validate(data)

    async def get_cards_errors(self, limit: int = 100, ascending: bool = False) -> CardErrorsResponse:
        """POST /content/v2/cards/error/list — карточки с ошибками создания."""
        body = {
            "cursor": {"limit": limit},
            "order": {"ascending": ascending},
        }
        data = await self._content.post("/content/v2/cards/error/list", json=body)
        return CardErrorsResponse.model_validate(data)

    async def update_cards(self, cards: list[dict]) -> dict:
        """
        POST /content/v2/cards/update — редактирование карточек.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ. Используй осторожно.
        """
        return await self._content.post("/content/v2/cards/update", json=cards)

    async def move_cards(self, target_imt_id: int, nm_ids: list[int]) -> dict:
        """
        POST /content/v2/cards/moveNm — объединение/разъединение карточек.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._content.post(
            "/content/v2/cards/moveNm",
            json={"targetIMT": target_imt_id, "nmIDs": nm_ids},
        )

    async def delete_cards_to_trash(self, nm_ids: list[int]) -> dict:
        """
        POST /content/v2/cards/delete/trash — перенести карточки в корзину.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._content.post("/content/v2/cards/delete/trash", json={"nmIDs": nm_ids})

    async def recover_cards_from_trash(self, nm_ids: list[int]) -> dict:
        """
        POST /content/v2/cards/recover — восстановить карточки из корзины.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._content.post("/content/v2/cards/recover", json={"nmIDs": nm_ids})

    async def get_trash_cards(self, request: CardsListRequest | None = None, locale: str = "ru") -> CardsListResponse:
        """POST /content/v2/get/cards/trash — список карточек в корзине."""
        body = request.model_dump(exclude_none=True) if request else {}
        data = await self._content.post(
            "/content/v2/get/cards/trash",
            json=body,
            params={"locale": locale},
        )
        return CardsListResponse.model_validate(data)

    async def get_cards_limits(self) -> CardLimitsResponse:
        """GET /content/v2/cards/limits — лимиты карточек товаров."""
        data = await self._content.get("/content/v2/cards/limits")
        return CardLimitsResponse.model_validate(data)

    async def generate_barcodes(self, count: int) -> BarcodesResponse:
        """POST /content/v2/barcodes — генерация баркодов (макс. 5000)."""
        data = await self._content.post("/content/v2/barcodes", json={"count": count})
        return BarcodesResponse.model_validate(data)

    async def create_cards(self, cards: list[dict]) -> dict:
        """
        POST /content/v2/cards/upload — создание карточек товаров.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._content.post("/content/v2/cards/upload", json=cards)

    async def create_cards_with_attach(self, imt_id: int, cards_to_add: list[dict]) -> dict:
        """
        POST /content/v2/cards/upload/add — создание карточек с присоединением.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._content.post(
            "/content/v2/cards/upload/add",
            json={"imtID": imt_id, "cardsToAdd": cards_to_add},
        )

    # ─── Медиа ───────────────────────────────────────────────────────────────

    async def upload_media_by_url(self, nm_id: int, urls: list[str]) -> dict:
        """
        POST /content/v3/media/save — загрузить медиафайлы по ссылкам.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._content.post(
            "/content/v3/media/save",
            json={"nmId": nm_id, "data": urls},
        )

    # ─── Цены и скидки ───────────────────────────────────────────────────────

    async def get_goods_list(
        self,
        limit: int = 100,
        offset: int = 0,
        filter_nm_id: int | None = None,
    ) -> GoodsListResponse:
        """
        GET /api/v2/list/goods/filter — список товаров с ценами и скидками.
        Хост: discounts-prices-api.wildberries.ru
        ✅ Работает с текущим токеном (скоуп: Цены и скидки, bit 4).
        """
        params = {"limit": limit, "offset": offset}
        if filter_nm_id is not None:
            params["filterNmID"] = filter_nm_id
        data = await self._prices.get("/api/v2/list/goods/filter", params=params)
        return GoodsListResponse.model_validate(data)

    async def get_goods_list_by_nm(self, nm_ids: list[int]) -> GoodsListResponse:
        """
        POST /api/v2/list/goods/filter — товары с ценами по списку артикулов.
        Хост: discounts-prices-api.wildberries.ru
        """
        data = await self._prices.post("/api/v2/list/goods/filter", json={"nmIDs": nm_ids})
        return GoodsListResponse.model_validate(data)

    async def get_goods_sizes(self, nm_id: int) -> dict:
        """
        GET /api/v2/list/goods/size/nm — цены по размерам конкретного артикула.
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.get("/api/v2/list/goods/size/nm", params={"nmId": nm_id})

    async def get_quarantine_goods(self, limit: int = 100, offset: int = 0) -> dict:
        """
        GET /api/v2/quarantine/goods — товары на карантине (заблокированные цены).
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.get(
            "/api/v2/quarantine/goods", params={"limit": limit, "offset": offset}
        )

    async def set_prices_and_discounts(self, tasks: list[dict]) -> dict:
        """
        POST /api/v2/upload/task — установить цены и скидки.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.post("/api/v2/upload/task", json={"data": tasks})

    async def set_prices_for_sizes(self, tasks: list[dict]) -> dict:
        """
        POST /api/v2/upload/task/size — установить цены для размеров.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.post("/api/v2/upload/task/size", json={"data": tasks})

    async def set_club_discounts(self, tasks: list[dict]) -> dict:
        """
        POST /api/v2/upload/task/club-discount — установить скидки WB Клуба.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.post("/api/v2/upload/task/club-discount", json={"data": tasks})

    async def get_price_upload_history(self, limit: int = 100, offset: int = 0) -> dict:
        """
        GET /api/v2/history/tasks — история загрузок цен.
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.get(
            "/api/v2/history/tasks", params={"limit": limit, "offset": offset}
        )

    async def get_price_upload_goods(self, upload_id: int) -> dict:
        """
        GET /api/v2/history/goods/task — товары конкретной загрузки цен.
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.get(
            "/api/v2/history/goods/task", params={"uploadID": upload_id}
        )

    async def get_price_buffer_tasks(self, limit: int = 100, offset: int = 0) -> dict:
        """
        GET /api/v2/buffer/tasks — задачи в буфере цен.
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.get(
            "/api/v2/buffer/tasks", params={"limit": limit, "offset": offset}
        )

    async def get_price_buffer_goods(self, upload_id: int) -> dict:
        """
        GET /api/v2/buffer/goods/task — товары задачи в буфере цен.
        Хост: discounts-prices-api.wildberries.ru
        """
        return await self._prices.get(
            "/api/v2/buffer/goods/task", params={"uploadID": upload_id}
        )

    # ─── Остатки и склады ────────────────────────────────────────────────────

    async def get_wb_offices(self) -> WBOfficesResponse:
        """
        GET /api/v3/offices — список офисов WB (пункты сдачи).
        Хост: marketplace-api.wildberries.ru
        WB возвращает список напрямую.
        """
        data = await self._market.get("/api/v3/offices")
        if isinstance(data, list):
            return WBOfficesResponse(result=data)
        return WBOfficesResponse.model_validate(data)

    async def get_seller_warehouses(self) -> SellerWarehousesResponse:
        """
        GET /api/v3/warehouses — склады продавца.
        Хост: marketplace-api.wildberries.ru
        WB возвращает список напрямую (не обёрнутый в объект).
        """
        data = await self._market.get("/api/v3/warehouses")
        # Реальный ответ — список, а не {result: [...]}
        if isinstance(data, list):
            return SellerWarehousesResponse(result=data)
        return SellerWarehousesResponse.model_validate(data)

    async def create_seller_warehouse(self, name: str, office_id: int) -> dict:
        """
        POST /api/v3/warehouses — создать склад продавца.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._market.post(
            "/api/v3/warehouses", json={"name": name, "officeId": office_id}
        )

    async def update_seller_warehouse(self, warehouse_id: int, name: str, office_id: int) -> dict:
        """
        PUT /api/v3/warehouses/{warehouseId} — обновить склад продавца.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._market.put(
            f"/api/v3/warehouses/{warehouse_id}",
            json={"name": name, "officeId": office_id},
        )

    async def delete_seller_warehouse(self, warehouse_id: int) -> dict:
        """
        DELETE /api/v3/warehouses/{warehouseId} — удалить склад продавца.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._market.delete(f"/api/v3/warehouses/{warehouse_id}")

    async def get_stocks(self, warehouse_id: int, skus: list[str]) -> dict:
        """
        POST /api/v3/stocks/{warehouseId} — получить остатки товаров на складе.
        Хост: marketplace-api.wildberries.ru
        ✅ Работает с текущим токеном (скоуп: Маркетплейс FBS, bit 8).
        """
        return await self._market.post(
            f"/api/v3/stocks/{warehouse_id}", json={"skus": skus}
        )

    async def update_stocks(self, warehouse_id: int, stocks: list[dict]) -> dict:
        """
        PUT /api/v3/stocks/{warehouseId} — обновить остатки на складе.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        Формат stocks: [{"sku": "...", "amount": N}]
        """
        return await self._market.put(
            f"/api/v3/stocks/{warehouse_id}", json={"stocks": stocks}
        )

    async def delete_stocks(self, warehouse_id: int, skus: list[str]) -> dict:
        """
        DELETE /api/v3/stocks/{warehouseId} — обнулить остатки на складе.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._market.delete(
            f"/api/v3/stocks/{warehouse_id}", json={"skus": skus}
        )

    async def get_dbw_contacts(self, warehouse_id: int) -> DBWContactsResponse:
        """
        GET /api/v3/dbw/warehouses/{warehouseId}/contacts — контакты склада DBW.
        Хост: marketplace-api.wildberries.ru
        """
        data = await self._market.get(f"/api/v3/dbw/warehouses/{warehouse_id}/contacts")
        return DBWContactsResponse.model_validate(data)

    async def update_dbw_contacts(self, warehouse_id: int, contacts: list[dict]) -> dict:
        """
        PUT /api/v3/dbw/warehouses/{warehouseId}/contacts — обновить контакты склада DBW.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._market.put(
            f"/api/v3/dbw/warehouses/{warehouse_id}/contacts",
            json={"contacts": contacts},
        )
