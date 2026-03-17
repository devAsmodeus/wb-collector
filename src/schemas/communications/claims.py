"""Схемы: Коммуникации — Претензии (возвраты покупателями)."""
from pydantic import BaseModel, Field


class ClaimItem(BaseModel):
    """Претензия от покупателя."""
    id: str | None = Field(None, description="ID претензии")
    createdDate: str | None = Field(None, description="Дата создания (ISO 8601)")
    state: str | None = Field(None, description="Статус претензии")
    text: str | None = Field(None, description="Текст претензии")
    productDetails: dict | None = Field(None, description="Данные товара")
    userName: str | None = Field(None, description="Имя покупателя")


class ClaimsResponse(BaseModel):
    """Список претензий."""
    data: dict | None = Field(None, description="Данные запроса (claims, countUnanswered)")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class UpdateClaimRequest(BaseModel):
    """Обработка претензии."""
    id: str = Field(description="ID претензии")
    wasViewed: bool | None = Field(None, description="Отметить как просмотренную")
    answer: dict | None = Field(None, description="Ответ продавца на претензию")
