import redis.asyncio as redis
from redis.asyncio import Redis

from core.settings import settings
# we create environment variable because redis aliased as redis in prod compose file
redis_storage: Redis = redis.Redis(host=settings.redis.host, port=settings.redis.port)


async def del_from_pattern(pattern: str) -> None:
    keys = await redis_storage.keys(pattern=pattern)
    for key in keys:
        await redis_storage.delete(key)
