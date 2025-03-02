from typing import AsyncGenerator
from fastapi import Depends
from redis import Redis
from app.core.cache.base import BaseRedisStorage
from app.core.cache.chat import ChatRedisStorage
from app.core.dependencies.connections.cache import RedisClient

async def get_session() -> AsyncGenerator[Redis, None]:
    client = RedisClient()
    redis = await client.connect()
    yield redis
    await client.close()

def get_redis_storage(redis: Redis = Depends(get_session)) -> BaseRedisStorage:
    """Предоставляет готовое хранилище Redis с соединением."""
    return BaseRedisStorage(redis)

def get_chat_redis_storage(redis: Redis = Depends(get_session)) -> ChatRedisStorage:
    """Предоставляет хранилище Redis для чата с соединением."""
    return ChatRedisStorage(redis)