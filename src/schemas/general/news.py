"""Схемы: Общее — АПИ новостей."""
from pydantic import BaseModel


class NewsTag(BaseModel):
    id: int
    name: str


class NewsItem(BaseModel):
    id: int
    header: str
    content: str
    date: str
    types: list[NewsTag] = []


class NewsResponse(BaseModel):
    data: list[NewsItem] = []
