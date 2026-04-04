with open('/app/src/services/fbw/sync/supplies.py') as f:
    content = f.read()

# Check how sync_supplies_full calls _fetch_goods
idx = content.find('sync_supplies_full')
print("sync_supplies_full uses _fetch_goods:", '_fetch_goods' in content[idx:idx+2000])

# Show _fetch_goods signature
idx2 = content.find('async def _fetch_goods')
print(content[idx2:idx2+150])

# Show how it's called in sync_supplies_incremental
idx3 = content.find('_fetch_goods(')
print("\nCall site:", content[idx3-50:idx3+150])

# Fix sync_supply_goods to call the module function directly
old = '''    async def sync_supply_goods(self, session) -> dict:
        """Публичный метод для Celery: загрузка товаров для всех поставок."""
        return await self._fetch_goods(session)'''

# Check what _fetch_goods needs - likely it needs collector + supply_id, not session
# So sync_supply_goods should replicate what sync_supplies_full does for goods
