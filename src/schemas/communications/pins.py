"""Схемы: Коммуникации — Закреплённые отзывы."""
from pydantic import BaseModel, Field


class PinnedFeedback(BaseModel):
    """Закреплённый отзыв."""
    id: str | None = Field(None, description="ID отзыва")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    text: str | None = Field(None, description="Текст отзыва")
    productValuation: int | None = Field(None, description="Оценка товара (1–5)")
    createdDate: str | None = Field(None, description="Дата создания (ISO 8601)")


class PinnedFeedbacksResponse(BaseModel):
    """Список закреплённых отзывов."""
    data: list[PinnedFeedback] | None = Field(None, description="Закреплённые отзывы")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class PinnedFeedbacksCount(BaseModel):
    """Количество закреплённых отзывов."""
    count: int | None = Field(None, description="Количество закреплённых отзывов")


class PinnedFeedbacksLimits(BaseModel):
    """Лимиты закреплённых отзывов."""
    total: int | None = Field(None, description="Общий лимит закреплённых отзывов")
    used: int | None = Field(None, description="Использовано слотов")


class PinFeedbackRequest(BaseModel):
    """Закрепить отзыв."""
    id: str = Field(description="ID отзыва для закрепления")
    nmId: int = Field(description="Артикул WB (nmID) к которому прикрепляется отзыв")


class UnpinFeedbackRequest(BaseModel):
    """Открепить отзыв."""
    id: str = Field(description="ID закреплённого отзыва для открепления")
