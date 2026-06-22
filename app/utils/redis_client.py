import redis.asyncio as aioredis

from app.config import settings

redis_client = aioredis.from_url(
    f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    if settings.REDIS_PASSWORD
    else f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    encoding="utf-8",
    decode_responses=True,
)


async def get_redis():
    """获取 Redis 客户端（用于依赖注入）"""
    return redis_client