from fastapi import Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.providers.database import get_session
from app.core.dependencies.providers.cache import get_chat_redis_storage
from app.core.integrations.cache.chat import ChatRedisStorage
from app.schemas import ChatResponse, ModelType
from app.services import ChatService
from app.routes.base import BaseRouter

class ChatRouter(BaseRouter):
    def __init__(self):
        super().__init__(prefix="chat", tags=["Chat"])

    def configure(self):
        @self.router.post("/completion", response_model=ChatResponse)
        async def get_chat_completion(
            model_type: ModelType = Form(None),
            message: str = Form(...),

            # current_user: UserCredentialsSchema = Depends(get_current_user),
            db_session: AsyncSession = Depends(get_session),
            chat_redis_storage: ChatRedisStorage = Depends(get_chat_redis_storage),
        ) -> ChatResponse:
            """
            # Получение ответа от YandexGPT

            ## Args
            * **model_type** - Тип модели (пока не работает, пользователя нет в базе данных)
            * **message** - Текст сообщения пользователя
            * **async_mode** - Использовать асинхронный режим (дешевле в 2 раза)
            * **current_user** - Данные текущего пользователя
            * **db_session** - Сессия базы данных

            ## Returns
            * **AIChatResponse** - Ответ от модели:
                * **success** - Признак успеха
                * **result** - Результат генерации:
                    * **alternatives** - Варианты ответа
                    * **usage** - Статистика использования токенов
                    * **modelVersion** - Версия модели

            ## Пример ответа
            ```json
            {
                "success": true,
                "result": {
                    "alternatives": [{
                        "message": {
                            "role": "assistant",
                            "text": "Ответ на ваш вопрос..."
                        },
                        "status": "ALTERNATIVE_STATUS_FINAL"
                    }],
                    "usage": {
                        "inputTextTokens": "19",
                        "completionTokens": "6",
                        "totalTokens": "25"
                    },
                    "modelVersion": "23.10.2024"
                }
            }
            ```
            """
            chat_service = ChatService(db_session, chat_redis_storage)
            return await chat_service.get_completion(message, model_type)#, current_user.id)