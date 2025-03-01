from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.connections.database import DatabaseContextManager


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор для получения сессии базы данных.

    Returns:
        AsyncGenerator[AsyncSession, None]: Генератор, возвращающий объект AsyncSession.
    """
    async with DatabaseContextManager() as session:
        try:
            yield session.session
            # Автоматический коммит при успешном выполнении
            await session.commit()
        except Exception:
            # При ошибке уже будет выполнен rollback в __aexit__
            raise
