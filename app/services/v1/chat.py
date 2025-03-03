import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.core.integrations.yandex_gpt.text import ChatHttpClient
from app.core.cache.chat import ChatRedisStorage
from app.schemas import (ChatRequest, ChatResponse, CompletionOptions,
                         Message, MessageRole)
from app.services.v1.base import BaseService

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
            # Получаем историю
            message_history = await self.storage.get_chat_history(user_id)

            # Создаем новое сообщение
            new_message = Message(role=role, text=message)

            # Добавляем новое сообщение в историю
            message_history.append(new_message)

            # Формируем полный список сообщений
            messages = [self.SYSTEM_MESSAGE] + message_history

            request = ChatRequest(
                modelUri=settings.yandex_model_uri,
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
