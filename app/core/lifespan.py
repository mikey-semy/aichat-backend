from contextlib import asynccontextmanager

from fastapi import FastAPI


class ApplicationLifecycle:
    """Управление жизненным циклом приложения"""

    def __init__(self):
        pass

    async def startup(self, app: FastAPI):
        """Запуск приложения"""
        pass

    async def shutdown(self, app: FastAPI):
        """Остановка приложения"""
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекстный менеджер жизненного цикла"""
    lifecycle = ApplicationLifecycle()
    await lifecycle.startup(app)
    yield
    await lifecycle.shutdown(app)
