"""DB: Общее — Пользователи."""
from litestar import Controller, get
from litestar.params import Parameter

from src.repositories.general.users import UsersRepository
from src.utils.db_manager import DBManager


class DbUsersController(Controller):
    path = "/users"
    tags = ["01. База данных"]

    @get(summary="Получить список пользователей из БД")
    async def get_users(
        self,
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            repo = UsersRepository(db.session)
            total = await repo.count()
            data = await repo.get_many(limit=limit, offset=offset)
            return {"data": [u.model_dump() for u in data], "total": total, "limit": limit, "offset": offset}
