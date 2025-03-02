from typing import AsyncGenerator
from fastapi import Depends
from redis import Redis
from app.core.cache.base import BaseRedisStorage
from app.core.dependencies.connections.cache import RedisClient

async def get_session() -> AsyncGenerator[Redis, None]:
    client = RedisClient()
    redis = await client.connect()
    yield redis
    await client.close()

def get_redis_storage(redis: Redis = Depends(get_session)) -> BaseRedisStorage:
    """Предоставляет готовое хранилище Redis с соединением."""
    return BaseRedisStorage(redis)
