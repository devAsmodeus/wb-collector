"""Схемы: Работа с товарами — Медиафайлы."""
from pydantic import BaseModel


class MediaUploadByUrlRequest(BaseModel):
    nmId: int
    data: list[str]  # список URL


class MediaUploadResponse(BaseModel):
    error: bool = False
    errorText: str = ""
