"""Схемы: Работа с товарами — Ярлыки."""
from typing import Any
from pydantic import BaseModel


class Tag(BaseModel):
    id: int
    name: str
    color: str


class TagCreate(BaseModel):
    name: str
    color: str


class TagUpdate(BaseModel):
    name: str | None = None
    color: str | None = None


class TagsResponse(BaseModel):
    error: bool = False
    errorText: str = ""
    data: list[Tag] | Any = None
