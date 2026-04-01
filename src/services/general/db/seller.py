"""Сервис DB: Общее — Чтение информации о продавце из БД."""
from src.schemas.general.seller import SellerInfo
from src.services.base import BaseService
from src.utils.db_manager import DBManager


class SellerDbService(BaseService):

    async def get_seller(self, db: DBManager) -> SellerInfo:
        """Возвращает данные о продавце из таблицы `sellers`."""
        return await db.seller.get_one()
