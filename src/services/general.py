import logging

from src.collectors.general import GeneralCollector
from src.schemas.seller import SellerInfo, NewsResponse, UsersResponse, InviteResponse
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class GeneralService(BaseService):

    async def ping(self) -> dict:
        """Проверка подключения к WB API."""
        async with GeneralCollector() as collector:
            return await collector.ping()

    async def sync_seller_info(self) -> SellerInfo:
        """Получить информацию о продавце из WB API и сохранить в БД."""
        async with GeneralCollector() as collector:
            seller = await collector.get_seller_info()
        async with self.db as db:
            result = await db.seller.upsert(seller)
            await db.commit()
        logger.info(f"Seller info synced: {result.name} ({result.sid})")
        return result

    async def get_news(
        self,
        from_date: str | None = None,
        from_id: int | None = None,
    ) -> NewsResponse:
        """Получить новости портала продавцов."""
        async with GeneralCollector() as collector:
            return await collector.get_news(from_date=from_date, from_id=from_id)

    async def get_users(
        self,
        limit: int = 100,
        offset: int = 0,
        invite_only: bool = False,
    ) -> UsersResponse:
        """Получить список пользователей продавца."""
        async with GeneralCollector() as collector:
            return await collector.get_users(
                limit=limit, offset=offset, invite_only=invite_only
            )

    async def invite_user(self, payload: dict) -> InviteResponse:
        """Создать приглашение для нового пользователя."""
        async with GeneralCollector() as collector:
            return await collector.invite_user(payload)

    async def update_users_access(self, users_accesses: list[dict]) -> None:
        """Изменить права доступа пользователей."""
        async with GeneralCollector() as collector:
            await collector.update_users_access(users_accesses)

    async def delete_user(self, user_id: int) -> None:
        """Удалить пользователя."""
        async with GeneralCollector() as collector:
            await collector.delete_user(user_id)
