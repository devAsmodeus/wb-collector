"""Тест 02-products — только read-only эндпоинты без DB."""
import asyncio, sys
sys.path.insert(0, "C:/Python/wb-collector")

from src.collectors.products import ProductsCollector


async def main():
    async with ProductsCollector() as c:

        print("=== GET /api/v2/list/goods/filter (цены) ===")
        goods = await c.get_goods_list(limit=5)
        items = goods.data.listGoods if goods.data else []
        print(f"  Товаров: {len(items)}")
        for g in items[:3]:
            sizes_prices = [s.price for s in g.sizes if s.price]
            print(f"  [{g.nmID}] {g.vendorCode} — скидка {g.discount}% — цены: {sizes_prices}")

        print("\n=== GET /api/v3/warehouses (склады продавца) ===")
        wh = await c.get_seller_warehouses()
        warehouses = wh.result or []
        print(f"  Складов: {len(warehouses)}")
        for w in warehouses:
            print(f"  [{w.id}] {w.name}")

        print("\n=== GET /api/v3/offices (офисы WB) ===")
        offices = await c.get_wb_offices()
        off_list = offices.result or []
        print(f"  Офисов: {len(off_list)}")
        if off_list:
            print(f"  Первый: {off_list[0].name}, {off_list[0].city}")

        print("\n=== GET /api/v2/history/tasks (история загрузок цен) ===")
        hist = await c.get_price_upload_history(limit=3)
        print(f"  Ответ: {hist}")

asyncio.run(main())
