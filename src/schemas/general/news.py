"""Схемы: Общее — Новости портала продавцов."""
from pydantic import BaseModel, Field


class NewsTag(BaseModel):
    id: int = Field(description="ID тега новости")
    name: str = Field(description="Название тега (напр. 'Обновления', 'Акции')")


class NewsItem(BaseModel):
    id: int = Field(description="Уникальный ID новости")
    header: str = Field(description="Заголовок новости")
    content: str = Field(description="Текст новости (HTML)")
    date: str = Field(description="Дата публикации (ISO 8601)")
    types: list[NewsTag] = Field(default=[], description="Теги / категории новости")


class NewsResponse(BaseModel):
    data: list[NewsItem] = Field(default=[], description="Список новостей")
