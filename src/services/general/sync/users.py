"""Сервис синхронизации: Пользователи продавца."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.general.users import UsersCollector
from src.repositories.general.users import UsersRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class UsersSyncService(BaseService):

    async def sync_users_full(self, session: AsyncSession) -> dict:
        """Полная синхронизация пользователей — загружает всех с пагинацией."""
        repo = UsersRepository(session)
        total_saved = 0
        limit = 100
        offset = 0

        async with UsersCollector() as collector:
            while True:
                response = await collector.get_users(limit=limit, offset=offset)
                users = response.users or []
                if not users:
                    break
                saved = await repo.upsert_many(users)
                total_saved += saved
                logger.info(f"Users sync: offset={offset}, batch={len(users)}, saved={saved}")
                if len(users) < limit:
                    break
                offset += limit

        return {"synced": total_saved, "source": "full"}

    async def sync_users_incremental(self, session: AsyncSession) -> dict:
        """Инкрементальная синхронизация — для пользователей идентична full
        (WB API не поддерживает фильтр по дате)."""
        return await self.sync_users_full(session)
