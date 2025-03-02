from typing import Any

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from app.core.settings import settings

from .base import BaseClient, BaseContextManager


class DatabaseClient(BaseClient):
    """Клиент для работы с базой данных"""

    def __init__(self, _settings: Any = settings) -> None:
        super().__init__()
        self._settings = _settings
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker | None = None

    def _create_engine(self) -> AsyncEngine:
        """Создает движок SQLAlchemy"""
        database_url = str(self._settings.database_dsn)
        return create_async_engine(
            database_url, **self._settings.engine_params
        )

    def _create_session_factory(self) -> async_sessionmaker:
        """Создает фабрику сессий"""
        return async_sessionmaker(bind=self._engine, **self._settings.session_params)

    async def connect(self) -> async_sessionmaker:
        """Инициализирует подключение к БД"""
        self._engine = self._create_engine()
        self._session_factory = self._create_session_factory()
        return self._session_factory

    async def close(self) -> None:
        """Закрывает подключение к БД"""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None


class DatabaseContextManager(BaseContextManager):
    """Контекстный менеджер для сессий БД"""

    def __init__(self) -> None:
        super().__init__()
        self.db_client = DatabaseClient()
        self.session: AsyncSession | None = None

    async def connect(self) -> AsyncSession:
        """Создаёт и возвращает сессию БД"""
        # Проверяем, не создана ли уже сессия
        if not self.session:
            session_factory = await self.db_client.connect()
            self.session = session_factory()
        return self.session

    async def close(self) -> None:
        """Закрывает сессию и подключение к БД"""
        if self.session:
            try:
                # Откатываем незафиксированные изменения
                await self.session.rollback()
            except Exception:
                # Обработка ошибок при откате
                pass
            finally:
                try:
                    # Закрываем сессию в любом случае
                    await self.session.close()
                except Exception:
                    # Обработка ошибок при закрытии
                    pass
                self.session = None

        # Закрываем клиент
        await self.db_client.close()

    async def commit(self) -> None:
        """Фиксирует изменения в БД"""
        if self.session:
            await self.session.commit()
