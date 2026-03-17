"""Сервис: Товары — Медиафайлы карточек."""
from src.collectors.products.media import MediaCollector
from src.collectors.products import ProductsCollector
from src.schemas.products.media import MediaUploadResponse
from src.services.base import BaseService


class MediaService(BaseService):

    async def upload_media_by_url(self, nm_id: int, urls: list[str]) -> MediaUploadResponse:
        async with ProductsCollector() as c:
            result = await c.media.upload_media_by_url(nm_id=nm_id, urls=urls)
        return MediaUploadResponse.model_validate(result)

    async def upload_media_file_placeholder(self, nm_id: int, photo_number: int) -> MediaUploadResponse:
        """Заглушка для file-upload — требует multipart, реализуется отдельно."""
        return MediaUploadResponse(
            error=True,
            errorText="Загрузка файлом недоступна через Swagger. Используйте upload-by-url или прямой запрос.",
        )
