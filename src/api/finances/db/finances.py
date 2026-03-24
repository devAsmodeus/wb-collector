"""DB: Finances — Чтение финансовых отчётов из БД."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.finances.db.finances import FinancesDbService
from src.utils.db_manager import DBManager


class DbFinancialReportController(Controller):
    path = "/"
    tags = ["DB / Finances"]

    @get(
        "/",
        summary="Финансовый отчёт из БД",
        description=(
            "Возвращает записи финансового отчёта из таблицы `wb_financial_report`.\n\n"
            "Перед первым вызовом выполните `POST /finances/sync/full/`."
        ),
    )
    async def get_financial_report(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Фильтр по дате продажи от"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Фильтр по дате продажи до"),
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FinancesDbService().get_financial_report(
                db.session, date_from=date_from, date_to=date_to, limit=limit, offset=offset
            )
