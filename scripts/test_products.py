"""Тест 02-products — read-only эндпоинты."""
import asyncio, sys
sys.path.insert(0, "C:/Python/wb-collector")

from src.collectors.products import ProductsCollector


async def main():
    async with ProductsCollector() as c:

        print("=== Цены: GET /api/v2/list/goods/filter ===")
        goods = await c.prices.get_goods_list(limit=5)
        items = goods.data.listGoods if goods.data else []
        print(f"  Товаров: {len(items)}")
        for g in items[:3]:
            prices = [s.price for s in g.sizes if s.price]
            print(f"  [{g.nmID}] {g.vendorCode} — скидка {g.discount}% — цены: {prices}")

        print("\n=== Склады: GET /api/v3/warehouses ===")
        wh = await c.warehouses.get_seller_warehouses()
        for w in (wh.result or []):
            print(f"  [{w.id}] {w.name}")

        print("\n=== Офисы WB: GET /api/v3/offices ===")
        offices = await c.warehouses.get_wb_offices()
        off_list = offices.result or []
        print(f"  Офисов: {len(off_list)}")

asyncio.run(main())
