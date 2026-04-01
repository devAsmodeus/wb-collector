"""Сервис Sync: FBW — Синхронизация поставок и товаров в поставках."""
import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.fbw.supplies import FBWSuppliesCollector
from src.repositories.fbw.supplies import FbwSuppliesRepository, FbwSupplyGoodsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


def _parse_datetime(value: str | None) -> datetime | None:
    """Парсит ISO 8601 дату из WB API."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


class FbwSuppliesSyncService(BaseService):

    async def sync_supplies_full(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех поставок FBW с товарами.
        Использует offset-based пагинацию: limit/offset.
        Для каждой поставки загружает список товаров.
        """
        supply_repo = FbwSuppliesRepository(session)
        goods_repo = FbwSupplyGoodsRepository(session)

        all_supplies = []
        all_goods = []

        async with FBWSuppliesCollector() as collector:
            offset = 0
            limit = 1000

            while True:
                response = await collector.get_supplies(payload={}, limit=limit, offset=offset)
                supplies = response.supplies or []

                if not supplies:
                    break

                for s in supplies:
                    supply_id = s.supplyID or s.preorderID
                    if supply_id is None:
                        continue

                    all_supplies.append({
                        "supply_id": supply_id,
                        "preorder_id": s.preorderID,
                        "status_id": s.statusID,
                        "box_type_id": s.boxTypeID,
                        "is_box_on_pallet": s.isBoxOnPallet,
                        "create_date": _parse_datetime(s.createDate),
                        "supply_date": _parse_datetime(s.supplyDate),
                        "fact_date": _parse_datetime(s.factDate),
                        "updated_date": _parse_datetime(s.updatedDate),
                        "phone": s.phone,
                        "raw_data": s.model_dump(),
                    })

                    # Загрузка товаров для каждой поставки
                    goods_offset = 0
                    while True:
                        goods_resp = await collector.get_supply_goods(
                            supply_id=supply_id, limit=1000, offset=goods_offset,
                        )
                        goods = goods_resp.goods or []
                        if not goods:
                            break

                        for g in goods:
                            all_goods.append({
                                "supply_id": supply_id,
                                "barcode": g.barcode,
                                "vendor_code": g.article,
                                "name": g.name,
                                "quantity": g.quantity,
                                "brand": g.brand,
                                "subject": g.subject,
                                "raw_data": g.model_dump(),
                            })

                        if len(goods) < 1000:
                            break
                        goods_offset += 1000

                if len(supplies) < limit:
                    break
                offset += limit

        saved_supplies = await supply_repo.upsert_many(all_supplies)
        saved_goods = await goods_repo.upsert_many(all_goods)

        logger.info(f"FBW supplies synced: {saved_supplies} supplies, {saved_goods} goods")
        return {
            "synced_supplies": saved_supplies,
            "synced_goods": saved_goods,
            "source": "full",
        }

    async def sync_supplies_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация поставок FBW.
        Загружает поставки, обновлённые после max(updated_date) из БД.
        Если БД пуста — fallback на полную синхронизацию.
        """
        supply_repo = FbwSuppliesRepository(session)
        max_updated = await supply_repo.get_max_updated_date()

        if max_updated is None:
            logger.info("FBW supplies incremental: no data in DB, falling back to full sync")
            result = await self.sync_supplies_full(session)
            result["source"] = "incremental_fallback_full"
            return result

        goods_repo = FbwSupplyGoodsRepository(session)
        all_supplies = []
        all_goods = []

        # Передаём диапазон дат для фильтрации
        date_from = max_updated.strftime("%Y-%m-%d")
        date_to = datetime.utcnow().strftime("%Y-%m-%d")
        payload = {"dates": [date_from, date_to]}

        async with FBWSuppliesCollector() as collector:
            offset = 0
            limit = 1000

            while True:
                response = await collector.get_supplies(payload=payload, limit=limit, offset=offset)
                supplies = response.supplies or []

                if not supplies:
                    break

                for s in supplies:
                    supply_id = s.supplyID or s.preorderID
                    if supply_id is None:
                        continue

                    all_supplies.append({
                        "supply_id": supply_id,
                        "preorder_id": s.preorderID,
                        "status_id": s.statusID,
                        "box_type_id": s.boxTypeID,
                        "is_box_on_pallet": s.isBoxOnPallet,
                        "create_date": _parse_datetime(s.createDate),
                        "supply_date": _parse_datetime(s.supplyDate),
                        "fact_date": _parse_datetime(s.factDate),
                        "updated_date": _parse_datetime(s.updatedDate),
                        "phone": s.phone,
                        "raw_data": s.model_dump(),
                    })

                    # Загрузка товаров для каждой поставки
                    goods_offset = 0
                    while True:
                        goods_resp = await collector.get_supply_goods(
                            supply_id=supply_id, limit=1000, offset=goods_offset,
                        )
                        goods = goods_resp.goods or []
                        if not goods:
                            break

                        for g in goods:
                            all_goods.append({
                                "supply_id": supply_id,
                                "barcode": g.barcode,
                                "vendor_code": g.article,
                                "name": g.name,
                                "quantity": g.quantity,
                                "brand": g.brand,
                                "subject": g.subject,
                                "raw_data": g.model_dump(),
                            })

                        if len(goods) < 1000:
                            break
                        goods_offset += 1000

                if len(supplies) < limit:
                    break
                offset += limit

        saved_supplies = await supply_repo.upsert_many(all_supplies)
        saved_goods = await goods_repo.upsert_many(all_goods)

        logger.info(
            f"FBW supplies incremental synced: {saved_supplies} supplies, "
            f"{saved_goods} goods (from_date={max_updated.isoformat()})"
        )
        return {
            "synced_supplies": saved_supplies,
            "synced_goods": saved_goods,
            "source": "incremental",
            "from_date": max_updated.isoformat(),
        }
