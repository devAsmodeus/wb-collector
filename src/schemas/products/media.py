"""Схемы: Товары — Медиафайлы карточек (фото, видео)."""
from pydantic import BaseModel, Field


class MediaUploadByUrlRequest(BaseModel):
    """Тело запроса для загрузки фото по URL."""
    nmId: int = Field(description="Артикул WB (nmID) карточки, к которой добавляем фото")
    data: list[str] = Field(
        description=(
            "Список URL изображений для загрузки.\n"
            "Порядок имеет значение — первый URL станет главным фото.\n"
            "Требования: JPEG/PNG, минимум 900×1200 px, максимум 15 МБ на фото."
        ),
        min_length=1,
        max_length=30,
    )


class MediaUploadResponse(BaseModel):
    """Ответ на загрузку медиафайлов."""
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки (если error=true)")
