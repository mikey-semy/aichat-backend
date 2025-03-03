import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.core.integrations.http.yandex_gpt.text import ChatHttpClient
from app.core.integrations.cache.chat import ChatRedisStorage
from app.schemas import (ChatRequest, ChatResponse, CompletionOptions,
                         Message, MessageRole, ModelType)
from app.services.v1.base import BaseService
from app.models import UserSettingsModel

logger = logging.getLogger(__name__)


class ChatService(BaseService):
    """
    Сервис для работы с чатом с AI

    Attributes:
        session: Сессия базы данных
        http_client: HTTP клиент для работы с AI API
    """

    def __init__(
        self,
        session: AsyncSession,
        storage: ChatRedisStorage,
    ):
        super().__init__(session)
        self.storage = storage
        self.http_client = ChatHttpClient()
        self.max_tokens = settings.YANDEX_MAX_TOKENS

    SYSTEM_MESSAGE = Message(role=MessageRole.SYSTEM.value, text=settings.YANDEX_PRE_INSTRUCTIONS)

    async def get_completion(
        self, message: str,
        user_id: int = 1, # временно, пока нет авторизации
        model_type: Optional[ModelType] = None,
        role: MessageRole = MessageRole.USER

    ) -> ChatResponse:
        """
        Получает ответ от модели на основе истории сообщений

        Args:
            request: Запрос к AI модели

        Returns:
            AIChatResponse: Ответ от модели
        """
        try:

            # Если модель не указана, получаем её из настроек пользователя
            if model_type is None:
                # Получаем настройки пользователя из БД
                user_settings = await self.get_user_settings(user_id)
                model_type = user_settings.preferred_model

                # В зависимости от выбранной модели формируем model_uri
                model_uri = self.get_model_uri(model_type)
            # Получаем историю
            message_history = await self.storage.get_chat_history(user_id)

            # Создаем новое сообщение
            new_message = Message(role=role, text=message)

            # Добавляем новое сообщение в историю
            message_history.append(new_message)

            # Формируем полный список сообщений
            messages = [self.SYSTEM_MESSAGE] + message_history

            request = ChatRequest(
                modelUri=model_uri,
                completionOptions=CompletionOptions(maxTokens=str(self.max_tokens)),
                messages=messages,
            )

            async with self.http_client as client:
                response = await client.get_completion(request)

                # Добавляем ответ ассистента в историю
                if response.success:
                    assistant_message = Message(
                        role=MessageRole.ASSISTANT,
                        text=response.result.alternatives[0].message.text,
                    )
                    message_history.append(assistant_message)

                    # Сохраняем обновленную историю
                    await self.storage.save_chat_history(user_id, message_history)

                return response
        except Exception as e:
            logger.error("Error in get_completion: %s", str(e))
            await self.storage.clear_chat_history(user_id)
            raise

    def get_model_uri(self, model_type: ModelType) -> str:
        """Формирует URI модели в зависимости от типа"""
        folder_id = settings.YANDEX_FOLDER_ID.get_secret_value()

        # Маппинг типов моделей на имена моделей
        model_mapping = {
            ModelType.YANDEX_GPT_LITE: "yandexgpt-lite",
            ModelType.YANDEX_GPT_PRO: "yandexgpt",
            ModelType.YANDEX_GPT_PRO_32K: "yandexgpt-32k",
            ModelType.LLAMA_8B: "llama-lite",
            ModelType.LLAMA_70B: "llama",
            ModelType.CUSTOM: "custom"  # Для кастомной модели нужна отдельная  логика
        }

        model_name = model_mapping.get(model_type, "llama")  # По умолчанию llama
        model_version = settings.YANDEX_MODEL_VERSION

        return f"gpt://{folder_id}/{model_name}/{model_version}"

    async def get_user_settings(self, user_id: int) -> UserSettingsModel:
        """
        Получает настройки пользователя или создаёт их, если не существуют

        Args:
            user_id: Идентификатор пользователя

        Returns:
            UserSettingsModel: Настройки пользователя

        TODO:
            - Перенести в data_manager
        """
        user_settings = await self.session.execute(
            select(UserSettingsModel).where(UserSettingsModel.user_id == user_id)
        )
        user_settings = user_settings.scalars().first()

        if not user_settings:
            # Создаём настройки со значениями по умолчанию
            user_settings = UserSettingsModel(user_id=user_id)
            self.session.add(user_settings)
            await self.session.commit()

        return user_settings
