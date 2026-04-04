with open('/app/src/services/fbw/sync/supplies.py') as f:
    content = f.read()

old = '''    async def sync_supply_goods(self, session) -> dict:
        """Публичный метод для Celery: загрузка товаров для всех поставок."""
        return await self._fetch_goods(session)'''

new = '''    async def sync_supply_goods(self, session) -> dict:
        """Загружает товары для ВСЕХ поставок из БД (1 запрос/поставку)."""
        from sqlalchemy import select
        from src.models.fbw import FbwSupply

        supply_repo = FbwSuppliesRepository(session)
        goods_repo = FbwSupplyGoodsRepository(session)

        result = await session.execute(select(FbwSupply.supply_id))
        supply_ids = [row[0] for row in result.fetchall()]

        if not supply_ids:
            return {"synced": 0, "synced_goods": 0}

        all_goods = []
        async with FBWSuppliesCollector() as collector:
            for sid in supply_ids:
                await _fetch_goods(collector, sid, all_goods)

        saved_goods = await goods_repo.upsert_many(all_goods)
        logger.info(f"FBW supply_goods sync: {saved_goods} goods for {len(supply_ids)} supplies")
        return {"synced": len(supply_ids), "synced_goods": saved_goods}'''

if old in content:
    content = content.replace(old, new)
    with open('/app/src/services/fbw/sync/supplies.py', 'w') as f:
        f.write(content)
    print("Fixed sync_supply_goods")
else:
    print("Not found")
    for i, line in enumerate(content.split('\n')[-10:], 1):
        print(f"{i}: {repr(line)}")
