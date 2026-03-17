"""Схемы: Коммуникации — Вопросы."""
from pydantic import BaseModel, Field


class QuestionCountUnanswered(BaseModel):
    """Количество неотвеченных вопросов."""
    count: int | None = Field(None, description="Количество неотвеченных вопросов")


class QuestionCount(BaseModel):
    """Статистика по вопросам."""
    answered: int | None = Field(None, description="Количество отвеченных вопросов")
    unanswered: int | None = Field(None, description="Количество неотвеченных вопросов")
    totalArchived: int | None = Field(None, description="Количество вопросов в архиве")


class QuestionItem(BaseModel):
    """Вопрос покупателя."""
    id: str | None = Field(None, description="ID вопроса")
    createdDate: str | None = Field(None, description="Дата создания (ISO 8601)")
    state: str | None = Field(None, description="Статус вопроса: `none` — новый, `wbRu` — отвечен WB, `answered` — отвечен продавцом")
    text: str | None = Field(None, description="Текст вопроса")
    productDetails: dict | None = Field(None, description="Данные товара")
    answer: dict | None = Field(None, description="Ответ продавца или WB")
    userName: str | None = Field(None, description="Имя покупателя")


class QuestionsResponse(BaseModel):
    """Список вопросов."""
    data: dict | None = Field(None, description="Данные запроса (questions, countUnanswered)")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class QuestionResponse(BaseModel):
    """Один вопрос."""
    data: dict | None = Field(None, description="Данные вопроса")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class AnswerQuestionRequest(BaseModel):
    """Ответ на вопрос / отклонение вопроса."""
    id: str = Field(description="ID вопроса")
    wasViewed: bool | None = Field(None, description="Отметить как просмотренный")
    isRejected: bool | None = Field(None, description="`true` — отклонить вопрос")
    answer: dict | None = Field(None, description="Текст ответа продавца")
