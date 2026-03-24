"""Сервис Sync: Товары — Синхронизация карточек товаров."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.products import ProductsCollector
from src.repositories.products.cards import CardsRepository
from src.schemas.products.cards import CardsListRequest
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class CardsSyncService(BaseService):

    async def sync_cards(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех карточек товаров.
        Использует cursor-based пагинацию: в каждом ответе приходит cursor
        с updatedAt и nmID, которые нужно передать в следующий запрос.
        Цикл продолжается, пока API возвращает карточки.
        """
        repo = CardsRepository(session)
        all_cards = []

        async with ProductsCollector() as collector:
            cursor_updated_at = None
            cursor_nm_id = None

            while True:
                settings = {"cursor": {"limit": 100}}
                if cursor_updated_at and cursor_nm_id:
                    settings["cursor"]["updatedAt"] = cursor_updated_at
                    settings["cursor"]["nmID"] = cursor_nm_id

                request = CardsListRequest(settings=settings)
                response = await collector.cards.get_cards_list(request)

                if not response.cards:
                    break

                all_cards.extend(response.cards)

                if response.cursor and response.cursor.updatedAt and response.cursor.nmID:
                    cursor_updated_at = response.cursor.updatedAt
                    cursor_nm_id = response.cursor.nmID
                else:
                    break

        saved = await repo.upsert_many(all_cards)
        logger.info(f"Cards synced: {saved} cards saved")
        return {"synced": saved, "source": "full"}
