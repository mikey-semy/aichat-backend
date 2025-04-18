import logging
from typing import Any, Dict
import json
import aiohttp
from .base import BaseClient, BaseContextManager

logger = logging.getLogger(__name__)

class HttpClient(BaseClient):
    """HTTP клиент"""

    async def connect(self) -> aiohttp.ClientSession:
        """Создает HTTP сессию"""
        logger.debug("Создание HTTP сессии...")
        self._client = aiohttp.ClientSession()
        return self._client

    async def close(self) -> None:
        """Закрывает HTTP сессию"""
        if self._client:
            logger.debug("Закрытие HTTP сессии...")
            await self._client.close()
            self._client = None

class HttpContextManager(BaseContextManager):
    """Контекстный менеджер для HTTP запросов"""

    def __init__(self, method: str, url: str, **kwargs) -> None:
        super().__init__()
        self.http_client = HttpClient()
        self.method = method
        self.url = url
        self.kwargs = kwargs

    async def connect(self) -> aiohttp.ClientSession:
        self._client = await self.http_client.connect()
        logger.debug("%s запрос к %s", self.method, self.url)

        if data := self.kwargs.get('data'):
            logger.debug("Request body: %s", json.dumps(data, indent=2))
            self.kwargs['data'] = {k: v for k, v in data.items() if v is not None}

        return self._client

    async def execute(self) -> Dict[str, Any]:
        """Выполняет HTTP запрос"""
        async with self._client.request(self.method, self.url, **self.kwargs) as response:
            return await response.json()
