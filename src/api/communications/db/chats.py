"""DB: Communications / Чаты."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.communications.db.chats import ChatsDbService
from src.utils.db_manager import DBManager


class DbChatsController(Controller):
    path = "/chats"
    tags = ["09. База данных"]

    @get(
        "/",
        summary="Чаты с покупателями из БД",
        description=(
            "Возвращает чаты из таблицы `chats` с пагинацией.\n\n"
            "Перед первым вызовом выполните `POST /communications/sync/chats/full`."
        ),
    )
    async def get_chats(
        self,
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await ChatsDbService().get_chats(db.session, limit=limit, offset=offset)
