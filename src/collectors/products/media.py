"""Коллектор: Работа с товарами — Медиафайлы (2 метода).
Хост: content-api.wildberries.ru
"""
from src.collectors.base import WBApiClient


class MediaCollector:
    def __init__(self, client: WBApiClient):
        self._client = client

    async def upload_media_by_url(self, nm_id: int, urls: list[str]) -> dict:
        """
        POST /content/v3/media/save — загрузить медиафайлы по ссылкам.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post(
            "/content/v3/media/save",
            json={"nmId": nm_id, "data": urls},
        )

    async def upload_media_file(self, nm_id: int, photo_number: int, file_bytes: bytes, filename: str = "photo.jpg") -> dict:
        """
        POST /content/v3/media/file — загрузить медиафайл напрямую (multipart/form-data).
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        Параметры: X-Nm-Id, X-Photo-Number в хедерах.
        """
        import httpx
        headers = {
            "Authorization": f"Bearer {self._client._token}",
            "X-Nm-Id": str(nm_id),
            "X-Photo-Number": str(photo_number),
        }
        async with httpx.AsyncClient() as client:
            files = {"uploadfile": (filename, file_bytes, "image/jpeg")}
            response = await client.post(
                f"{self._client._base_url}/content/v3/media/file",
                headers=headers,
                files=files,
            )
            return response.json()
