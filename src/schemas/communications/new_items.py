"""Схемы: Коммуникации — Новые вопросы/отзывы (общая лента)."""
from pydantic import BaseModel, Field


class NewFeedbacksQuestions(BaseModel):
    """Новые вопросы и отзывы."""
    feedbacks: int | None = Field(None, description="Количество новых необработанных отзывов")
    questions: int | None = Field(None, description="Количество новых необработанных вопросов")


class NewFeedbacksQuestionsResponse(BaseModel):
    """Ответ: новые вопросы и отзывы."""
    data: NewFeedbacksQuestions | None = Field(None, description="Счётчики новых отзывов и вопросов")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")
