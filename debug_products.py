import asyncio
from src.utils.db_manager import DBManager
from src.services.products.sync.warehouses import WarehousesSyncService
from src.services.products.sync.directories import DirectoriesSyncService

async def test():
    print("=== WAREHOUSES ===")
    try:
        async with DBManager() as db:
            r = await WarehousesSyncService().sync_warehouses(db.session)
            print('OK:', r)
    except Exception as e:
        import traceback; traceback.print_exc()

    print("=== CATEGORIES ===")
    try:
        async with DBManager() as db:
            r = await DirectoriesSyncService().sync_categories(db.session)
            print('OK:', r)
    except Exception as e:
        import traceback; traceback.print_exc()

asyncio.run(test())
