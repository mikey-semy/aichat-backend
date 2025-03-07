import json
import logging
from typing import Any, Dict, Optional

import aiohttp


class BaseHttpClient:
    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    async def __aenter__(self) -> "BaseHttpClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None
            self.logger.debug("Сессия закрыта")

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self._session:
            self._session = aiohttp.ClientSession()
        return self._session

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            session = await self._get_session()
            self.logger.debug("GET запрос к %s", url)
            async with session.get(url, headers=headers, params=params) as resp:
                return await resp.json()
        finally:
            await self.close()

    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            self.logger.debug("POST request body: %s", json.dumps(data, indent=2))
            if data:
                # Фильтруем None значения из параметров
                data = {k: v for k, v in data.items() if v is not None}

            session = await self._get_session()
            self.logger.debug("POST запрос к %s с данными %s", url, data)
            # Проверяем Content-Type
            if (
                headers
                and headers.get("Content-Type") == "application/x-www-form-urlencoded"
            ):
                # Для OAuth используем data как есть
                async with session.post(url, data=data, headers=headers) as resp:
                    return await resp.json()
            else:
                # Для остальных запросов используем json
                async with session.post(url, json=data, headers=headers) as resp:
                    return await resp.json()
        finally:
            await self.close()
