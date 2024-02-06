import redis.asyncio as redis

from core.settings import settings

redis_storage = redis.Redis(username=settings.redis.user_name)


async def del_from_pattern(pattern: str) -> None:
    keys = await redis_storage.keys(pattern=pattern)
    for key in keys:
        await redis_storage.delete(key)