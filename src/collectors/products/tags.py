"""Коллектор: Работа с товарами — Ярлыки (5 методов).
Хост: content-api.wildberries.ru
"""
from src.collectors.base import WBApiClient
from src.schemas.products.tags import TagsResponse


class TagsCollector:
    def __init__(self, client: WBApiClient):
        self._client = client

    async def get_tags(self) -> TagsResponse:
        """GET /content/v2/tags — список ярлыков."""
        data = await self._client.get("/content/v2/tags")
        return TagsResponse.model_validate(data)

    async def create_tag(self, name: str, color: str) -> dict:
        """POST /content/v2/tag — создать ярлык."""
        return await self._client.post("/content/v2/tag", json={"name": name, "color": color})

    async def update_tag(self, tag_id: int, name: str | None = None, color: str | None = None) -> dict:
        """PATCH /content/v2/tag/{id} — изменить ярлык."""
        body = {}
        if name is not None:
            body["name"] = name
        if color is not None:
            body["color"] = color
        return await self._client.patch(f"/content/v2/tag/{tag_id}", json=body)

    async def delete_tag(self, tag_id: int) -> dict:
        """DELETE /content/v2/tag/{id} — удалить ярлык."""
        return await self._client.delete(f"/content/v2/tag/{tag_id}")

    async def link_tags_to_card(self, nm_id: int, tag_ids: list[int]) -> dict:
        """POST /content/v2/tag/nomenclature/link — привязать ярлыки к карточке."""
        return await self._client.post(
            "/content/v2/tag/nomenclature/link",
            json={"nmID": nm_id, "tagsIDs": tag_ids},
        )
