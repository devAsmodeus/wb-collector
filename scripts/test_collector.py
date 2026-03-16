"""Быстрый тест всех методов 01-general без БД."""
import asyncio
import sys
sys.path.insert(0, "C:/Python/wb-collector")

from src.collectors.general import GeneralCollector


async def main():
    async with GeneralCollector() as c:

        print("=== ping ===")
        print(await c.ping())

        print("\n=== seller-info ===")
        s = await c.get_seller_info()
        print(f"  {s.name} | {s.tradeMark} | ИНН {s.itn}")

        print("\n=== news ===")
        news = await c.get_news(from_date="2026-01-01")
        print(f"  Новостей: {len(news.data)}")
        if news.data:
            n = news.data[0]
            print(f"  Последняя: [{n.id}] {n.date} — {n.header[:60]}")

        print("\n=== users (активные) ===")
        users = await c.get_users(limit=10)
        print(f"  Всего: {users.total}, в ответе: {users.countInResponse}")
        for u in users.users:
            print(f"  [{u.id}] {u.firstName} {u.secondName} | {u.email} | owner={u.isOwner}")

        print("\n=== users (приглашённые) ===")
        invited = await c.get_users(limit=10, invite_only=True)
        print(f"  Приглашённых: {invited.total}")

asyncio.run(main())
