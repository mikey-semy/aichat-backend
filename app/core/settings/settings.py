import logging
from typing import Any, Dict, List

from pydantic import SecretStr, RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.lifespan import lifespan
from app.core.settings.logging import LoggingSettings
from app.core.settings.paths import PathConfig

env_file_path, app_env = PathConfig.get_env_file_and_type()

logger = logging.getLogger(__name__)
class Settings(BaseSettings):

    # Виртуальное окружение приложения
    app_env: str = app_env

    logging: LoggingSettings = LoggingSettings()

    # Настройки приложения
    TITLE: str = "AI Chat"
    DESCRIPTION: str = "AI Chat API"
    VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    @property
    def app_params(self) -> dict:
        """
        Параметры для инициализации FastAPI приложения.

        Returns:
            Dict с настройками FastAPI
        """
        return {
            "title": self.TITLE,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "swagger_ui_parameters": {"defaultModelsExpandDepth": -1},
            "root_path": "",
            "lifespan": lifespan,
        }

    @property
    def uvicorn_params(self) -> dict:
        """
        Параметры для запуска uvicorn сервера.

        Returns:
            Dict с настройками uvicorn
        """
        return {
            "host": self.HOST,
            "port": self.PORT,
            "proxy_headers": True,
            "log_level": self.logging.LEVEL.lower(),
        }

    # Настройки JWT
    TOKEN_TYPE: str = "Bearer"
    TOKEN_EXPIRE_MINUTES: int = 1440
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_SECRET_KEY: SecretStr

    # Настройки доступа в docs/redoc
    DOCS_ACCESS: bool = True
    DOCS_USERNAME: str = "admin"
    DOCS_PASSWORD: SecretStr = "admin"

    # Настройки базы данных
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @property
    def database_dsn(self) -> PostgresDsn:
        database_dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return database_dsn

    @property
    def database_url(self) -> str:
        """
        Для alembic нужно строку с подключением к БД
        """
        database_dsn = str(self.database_dsn)
        return database_dsn

    @property
    def engine_params(self) -> Dict[str, Any]:
        """
        Формирует параметры для создания SQLAlchemy engine
        """
        return {
            "echo": True,
        }

    @property
    def session_params(self) -> Dict[str, Any]:
        """
        Формирует параметры для создания SQLAlchemy session
        """
        return {
            "autocommit": False,
            "autoflush": False,
            "expire_on_commit": False,
            "class_": AsyncSession,
        }

    # Настройки Yandex GPT
    YANDEX_PRE_INSTRUCTIONS: str = "Ты ассистент, помогающий пользователю."
    YANDEX_TEMPERATURE: float = 0.6
    YANDEX_MAX_TOKENS: int = 2000
    YANDEX_MODEL_NAME: str = "llama"
    YANDEX_MODEL_VERSION: str = "rc"
    YANDEX_API_URL: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    YANDEX_API_KEY: SecretStr
    YANDEX_PRIVATE_KEY: SecretStr
    YANDEX_KEY_ID: SecretStr
    YANDEX_FOLDER_ID: SecretStr

    @property
    def yandex_model_uri(self) -> str:
        """
        Формирует URI модели Yandex GPT.

        Returns:
            str: URI в формате gpt://{folder_id}/{model_name}/{model_version}
        """
        return f"gpt://{self.YANDEX_FOLDER_ID.get_secret_value()}/{self.YANDEX_MODEL_NAME}/{self.YANDEX_MODEL_VERSION}"

    # Настройки Redis
    REDIS_USER: str = "default"
    REDIS_PASSWORD: SecretStr
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_POOL_SIZE: int = 10

    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USER,
            password=self.REDIS_PASSWORD.get_secret_value(),
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=f"/{self.REDIS_DB}"
        )

    @property
    def redis_url(self) -> str:
        return str(self.redis_dsn)

    @property
    def redis_params(self) -> Dict[str, Any]:
        return {
            "url": self.redis_url,
            "max_connections": self.REDIS_POOL_SIZE
        }

    # Настройки CORS
    ALLOW_ORIGINS: List[str] = []
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]

    @property
    def cors_params(self) -> Dict[str, Any]:
        """
        Формирует параметры CORS для FastAPI.

        Returns:
            Dict с настройками CORS middleware
        """
        return {
            "allow_origins": self.ALLOW_ORIGINS,
            "allow_credentials": self.ALLOW_CREDENTIALS,
            "allow_methods": self.ALLOW_METHODS,
            "allow_headers": self.ALLOW_HEADERS,
        }

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="allow",
    )
