with open('/app/src/api/fbw/sync/supplies.py') as f:
    content = f.read()

# Add supply_goods sync endpoint
new_endpoint = '''
    @post(
        "/supply-goods",
        summary="Синхронизация товаров в поставках FBW",
        description="Загружает товары для всех поставок FBW из WB API. Тяжёлая операция — 1 запрос на поставку.",
    )
    async def sync_supply_goods(self) -> dict:
        async with DBManager() as db:
            return await FbwSuppliesSyncService().sync_supply_goods(db.session)
'''

# Insert before the last closing of the class (before the last empty line or end)
content = content.rstrip() + '\n' + new_endpoint

with open('/app/src/api/fbw/sync/supplies.py', 'w') as f:
    f.write(content)
print("Added /supply-goods endpoint")
