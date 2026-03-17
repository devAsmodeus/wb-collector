"""Схемы: Коммуникации — Отзывы."""
from pydantic import BaseModel, Field


class FeedbackCountUnanswered(BaseModel):
    """Количество необработанных отзывов."""
    count: int | None = Field(None, description="Количество новых необработанных отзывов")


class FeedbackCount(BaseModel):
    """Статистика по отзывам."""
    answered: int | None = Field(None, description="Количество отвеченных отзывов")
    unanswered: int | None = Field(None, description="Количество неотвеченных отзывов")
    totalArchived: int | None = Field(None, description="Количество отзывов в архиве")


class FeedbackItem(BaseModel):
    """Отзыв покупателя."""
    id: str | None = Field(None, description="ID отзыва")
    createdDate: str | None = Field(None, description="Дата создания (ISO 8601)")
    productValuation: int | None = Field(None, description="Оценка товара (1–5)")
    wasViewed: bool | None = Field(None, description="Просмотрен ли отзыв")
    isAbleToChangeMyGrade: bool | None = Field(None, description="Можно ли изменить оценку")
    text: str | None = Field(None, description="Текст отзыва")
    productDetails: dict | None = Field(None, description="Данные товара")
    answer: dict | None = Field(None, description="Ответ продавца")
    photo: list[dict] | None = Field(None, description="Фотографии в отзыве")
    video: list[dict] | None = Field(None, description="Видео в отзыве")
    userName: str | None = Field(None, description="Имя покупателя")


class FeedbacksResponse(BaseModel):
    """Список отзывов."""
    data: dict | None = Field(None, description="Данные запроса (feedbacks, countUnanswered)")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class FeedbackResponse(BaseModel):
    """Один отзыв."""
    data: dict | None = Field(None, description="Данные отзыва")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class AnswerFeedbackRequest(BaseModel):
    """Ответ на отзыв."""
    id: str = Field(description="ID отзыва")
    text: str = Field(description="Текст ответа продавца")


class UpdateFeedbackAnswerRequest(BaseModel):
    """Редактирование ответа на отзыв."""
    id: str = Field(description="ID отзыва")
    text: str = Field(description="Новый текст ответа")
