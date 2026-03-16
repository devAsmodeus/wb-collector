"""Быстрый тест коллектора без БД."""
import asyncio
import sys
sys.path.insert(0, "C:/Python/wb-collector")

from src.collectors.general import GeneralCollector


async def main():
    async with GeneralCollector() as collector:
        print("=== ping ===")
        ping = await collector.ping()
        print(ping)

        print("\n=== seller-info ===")
        seller = await collector.get_seller_info()
        print(f"  name:       {seller.name}")
        print(f"  sid:        {seller.sid}")
        print(f"  tradeMark:  {seller.tradeMark}")
        print(f"  itn:        {seller.itn}")

asyncio.run(main())
