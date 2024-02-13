import redis.asyncio as redis
from redis.asyncio import Redis

from core.settings import settings

redis_storage: Redis = redis.Redis(username=settings.redis.user_name, host='localhost')


async def del_from_pattern(pattern: str) -> None:
    keys = await redis_storage.keys(pattern=pattern)
    for key in keys:
        await redis_storage.delete(key)
