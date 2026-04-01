"""
Контроллер: Коммуникации / Чат с покупателями
WB API: feedbacks-api.wildberries.ru
Tag: Чат с покупателями (4 endpoints)
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.communications.chat import SendMessageRequest
from src.services.communications.wb.chat import ChatService


class ChatController(Controller):
    path = "/chat"
    tags = ["09. API Wildberries"]

    @get(
        "/chats",
        summary="Список чатов с покупателями",
        description=(
            "Возвращает список активных чатов с покупателями.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/seller/chats`"
        ),
    )
    async def get_chats(
        self,
        limit: int = Parameter(10, query="take", description="Количество чатов. По умолчанию: 10."),
        offset: int = Parameter(0, query="skip", description="Смещение. По умолчанию: 0."),
    ) -> dict:
        return await ChatService().get_chats(limit, offset)

    @get(
        "/events",
        summary="События чата",
        description=(
            "Возвращает сообщения и события в конкретном чате с покупателем.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/seller/events`"
        ),
    )
    async def get_events(
        self,
        chat_id: str = Parameter(query="chatId", description="ID чата"),
        limit: int = Parameter(10, query="take", description="Количество событий. По умолчанию: 10."),
        offset: int = Parameter(0, query="skip", description="Смещение. По умолчанию: 0."),
    ) -> dict:
        return await ChatService().get_events(chat_id, limit, offset)

    @post(
        "/message",
        summary="Отправить сообщение в чат",
        description=(
            "Отправляет сообщение покупателю в чате.\n\n"
            "**WB endpoint:** `POST feedbacks-api.wildberries.ru/api/v1/seller/message`"
        ),
    )
    async def send_message(self, data: SendMessageRequest) -> dict:
        return await ChatService().send_message(data)

    @get(
        "/download/{file_id:str}",
        summary="Скачать файл из чата",
        description=(
            "Возвращает файл, прикреплённый к сообщению в чате.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/seller/download/{id}`"
        ),
    )
    async def download_file(
        self,
        file_id: str = Parameter(description="ID файла"),
    ) -> dict:
        return await ChatService().download_file(file_id)
