"""Коллектор: Работа с товарами — Категории, предметы, характеристики (10 методов).
Хост: content-api.wildberries.ru
"""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.products.directories import (
    ParentCategoriesResponse, SubjectsResponse, SubjectCharcsResponse,
    TnvedResponse, BrandsResponse,
)


class DirectoriesCollector:
    def __init__(self, client: WBApiClient):
        self._client = client

    async def get_parent_categories(self, locale: str = "ru") -> ParentCategoriesResponse:
        """GET /content/v2/object/parent/all — родительские категории товаров."""
        data = await self._client.get("/content/v2/object/parent/all", params={"locale": locale})
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
        data = await self._client.get("/content/v2/object/all", params=params)
        return SubjectsResponse.model_validate(data)

    async def get_subject_charcs(self, subject_id: int, locale: str = "ru") -> SubjectCharcsResponse:
        """GET /content/v2/object/charcs/{subjectId} — характеристики предмета."""
        data = await self._client.get(
            f"/content/v2/object/charcs/{subject_id}", params={"locale": locale}
        )
        return SubjectCharcsResponse.model_validate(data)

    async def get_colors(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/colors — цвета."""
        return await self._client.get("/content/v2/directory/colors", params={"locale": locale})

    async def get_kinds(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/kinds — пол."""
        return await self._client.get("/content/v2/directory/kinds", params={"locale": locale})

    async def get_countries(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/countries — страны производства."""
        return await self._client.get("/content/v2/directory/countries", params={"locale": locale})

    async def get_seasons(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/seasons — сезоны."""
        return await self._client.get("/content/v2/directory/seasons", params={"locale": locale})

    async def get_vat_rates(self, locale: str = "ru") -> dict:
        """GET /content/v2/directory/vat — ставки НДС."""
        return await self._client.get("/content/v2/directory/vat", params={"locale": locale})

    async def get_tnved(self, subject_id: int, search: int | None = None, locale: str = "ru") -> TnvedResponse:
        """GET /content/v2/directory/tnved — ТНВЭД-коды предмета."""
        params = {"subjectID": subject_id, "locale": locale}
        if search is not None:
            params["search"] = search
        data = await self._client.get("/content/v2/directory/tnved", params=params)
        return TnvedResponse.model_validate(data)

    async def get_brands(self, subject_id: int, next_cursor: int | None = None) -> BrandsResponse:
        """GET /api/content/v1/brands — бренды предмета."""
        params = {"subjectId": subject_id}
        if next_cursor is not None:
            params["next"] = next_cursor
        data = await self._client.get("/api/content/v1/brands", params=params)
        return BrandsResponse.model_validate(data)
