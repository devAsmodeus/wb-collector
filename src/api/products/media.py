"""
Контроллер: Products / Медиафайлы
WB API: content-api.wildberries.ru

Загрузка фотографий к карточкам товаров — по URL или файлом.
"""
from litestar import Controller, post
from litestar.params import Parameter

from src.schemas.products.media import MediaUploadByUrlRequest, MediaUploadResponse
from src.services.products.media import MediaService


class MediaController(Controller):
    path = "/media"
    tags = ["Products — Карточки"]

    @post(
        "/upload-by-url",
        summary="Загрузить фото по URL",
        description=(
            "Загружает фотографии к карточке товара по внешним URL.\n\n"
            "**Порядок URL важен** — первый URL станет главным фото карточки.\n\n"
            "**Требования к изображениям:**\n"
            "- Формат: JPEG или PNG\n"
            "- Минимальный размер: 900×1200 px\n"
            "- Максимум: 30 фото на карточку\n"
            "- Вес: до 15 МБ на фото\n\n"
            "⚠️ Фото обрабатываются асинхронно — появятся в карточке через несколько секунд.\n\n"
            "**WB endpoint:** `POST content-api.wildberries.ru/content/v3/media/save`"
        ),
    )
    async def upload_by_url(self, data: MediaUploadByUrlRequest) -> MediaUploadResponse:
        return await MediaService().upload_media_by_url(
            nm_id=data.nmId,
            urls=data.data,
        )

    @post(
        "/upload-file/{nm_id:int}/{photo_number:int}",
        summary="Загрузить фото файлом (multipart)",
        description=(
            "Загружает фотографию к карточке товара как бинарный файл (multipart/form-data).\n\n"
            "**Параметры пути:**\n"
            "- `nm_id` — артикул WB карточки\n"
            "- `photo_number` — порядковый номер фото (1 = главное, 2–30 = дополнительные)\n\n"
            "**Требования к файлу:**\n"
            "- Формат: JPEG или PNG\n"
            "- Минимальный размер: 900×1200 px\n"
            "- Максимальный вес: 15 МБ\n\n"
            "⚠️ Используйте этот метод если у вас нет публичных URL для фото.\n\n"
            "**WB endpoint:** `POST content-api.wildberries.ru/content/v3/media/file`"
        ),
    )
    async def upload_file(
        self,
        nm_id: int = Parameter(description="Артикул WB (nmID) карточки"),
        photo_number: int = Parameter(
            description="Номер фото в карточке: 1 — главное, 2–30 — дополнительные.",
            ge=1,
            le=30,
        ),
    ) -> MediaUploadResponse:
        # Файловая загрузка через сырой endpoint — реализация в сервисе
        return await MediaService().upload_media_file_placeholder(nm_id, photo_number)
