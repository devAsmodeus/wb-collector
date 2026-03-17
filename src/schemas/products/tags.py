"""Схемы: Товары — Теги карточек товаров."""
from typing import Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Response схемы
# ---------------------------------------------------------------------------

class WBTag(BaseModel):
    """Тег карточки товара."""
    id: int = Field(description="Уникальный ID тега")
    name: str = Field(description="Название тега (напр. 'Акция', 'Новинка', 'Хит продаж')")
    color: str = Field(
        description=(
            "Цвет тега в HEX-формате без `#` (напр. `D41D1D` — красный, `1DD44A` — зелёный). "
            "Отображается в интерфейсе кабинета продавца."
        )
    )


class TagsResponse(BaseModel):
    """Ответ со списком тегов."""
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки (если error=true)")
    data: list[WBTag] | Any = Field(None, description="Список тегов продавца")


# ---------------------------------------------------------------------------
# Request схемы
# ---------------------------------------------------------------------------

class TagCreateRequest(BaseModel):
    """Тело запроса для создания нового тега."""
    name: str = Field(
        description="Название тега. Максимум 20 символов.",
        max_length=20,
    )
    color: str = Field(
        description=(
            "Цвет тега в HEX-формате без `#` (6 символов). "
            "Напр. `D41D1D` — красный, `1DD44A` — зелёный, `1D72D4` — синий."
        ),
        min_length=6,
        max_length=6,
    )


class TagUpdateRequest(BaseModel):
    """Тело запроса для переименования / смены цвета тега."""
    name: str | None = Field(
        None,
        description="Новое название тега. Если не указано — название не меняется.",
        max_length=20,
    )
    color: str | None = Field(
        None,
        description=(
            "Новый цвет тега в HEX-формате без `#` (6 символов). "
            "Если не указан — цвет не меняется."
        ),
        min_length=6,
        max_length=6,
    )


class TagLinkRequest(BaseModel):
    """Тело запроса для привязки / отвязки тегов к карточке товара."""
    nmID: int = Field(
        description="Артикул WB (nmID) карточки товара, к которой привязываем теги."
    )
    tagIDs: list[int] = Field(
        description=(
            "Список ID тегов для привязки к карточке. "
            "Передайте пустой список `[]` чтобы отвязать все теги от карточки."
        ),
    )
