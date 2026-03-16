import redis.asyncio as aioredis
from src.config import settings


class RedisManager:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = aioredis.from_url(settings.redis_url, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.aclose()
