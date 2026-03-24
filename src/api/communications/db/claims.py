"""DB: Communications / Претензии."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.communications.db.claims import ClaimsDbService
from src.utils.db_manager import DBManager


class DbClaimsController(Controller):
    path = "/claims"
    tags = ["DB / Communications"]

    @get(
        "/",
        summary="Претензии из БД",
        description=(
            "Возвращает претензии из таблицы `wb_claims` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /communications/sync/claims/full`."
        ),
    )
    async def get_claims(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Дата начала (ISO 8601)"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Дата окончания (ISO 8601)"),
        status: str | None = Parameter(default=None, query="status", description="Фильтр по статусу претензии"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await ClaimsDbService().get_claims(
                db.session,
                date_from=date_from,
                date_to=date_to,
                status=status,
                limit=limit,
                offset=offset,
            )
