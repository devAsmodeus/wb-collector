"""Схемы: Коммуникации — Чат с покупателями."""
from pydantic import BaseModel, Field


class ChatItem(BaseModel):
    """Чат с покупателем."""
    id: str | None = Field(None, description="ID чата")
    orderId: str | None = Field(None, description="ID заказа")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    createdDate: str | None = Field(None, description="Дата создания чата (ISO 8601)")
    lastMessage: dict | None = Field(None, description="Последнее сообщение в чате")
    unreadCount: int | None = Field(None, description="Количество непрочитанных сообщений")


class ChatsResponse(BaseModel):
    """Список чатов с покупателями."""
    data: dict | None = Field(None, description="Чаты (chats, total, hasMore)")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class ChatEvent(BaseModel):
    """Событие в чате."""
    type: str | None = Field(None, description="Тип события")
    createdDate: str | None = Field(None, description="Дата события (ISO 8601)")
    message: dict | None = Field(None, description="Содержимое сообщения")


class ChatEventsResponse(BaseModel):
    """События чата."""
    data: dict | None = Field(None, description="События чата (events, hasMore)")
    error: bool | None = Field(None, description="Признак ошибки")
    errorText: str | None = Field(None, description="Текст ошибки")


class SendMessageRequest(BaseModel):
    """Отправка сообщения в чат."""
    chatId: str = Field(description="ID чата")
    message: str = Field(description="Текст сообщения")
    files: list[str] | None = Field(None, description="ID файлов для вложений")


class ReturnOrderRequest(BaseModel):
    """Запрос на возврат заказа."""
    id: str = Field(description="ID отзыва, по которому запрашивается возврат")
