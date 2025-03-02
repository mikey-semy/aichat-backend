from app.core.settings import settings
from app.core.exceptions import ChatAuthError, ChatCompletionError
from app.schemas import ChatRequest, ChatResponse, Result

from ..base import BaseHttpClient


class ChatHttpClient(BaseHttpClient):
    """
    Класс для работы с API Yandex
    """

    async def get_completion(self, chat_request: ChatRequest) -> ChatResponse:
        """
        Получение ответа от Yandex API

        Args:
            chat_request: Запрос к API

        Returns:
            AIChatResponse: Ответ от API

        Raises:
            HTTPException: При ошибках запроса
        """
        headers = {
            "Authorization": f"Api-Key {settings.YANDEX_API_KEY.get_secret_value()}",
            "Content-Type": "application/json",
        }

        if not settings.YANDEX_API_KEY.get_secret_value():
            raise ChatAuthError("API ключ не задан")

        chat_request.modelUri = settings.yandex_model_uri

        try:
            request_data = chat_request.model_dump(by_alias=True)
            for msg in request_data["messages"]:
                msg["role"] = msg["role"].value

            self.logger.debug("Request data: %s", request_data)

            response = await self.post(
                url=settings.YANDEX_API_URL, headers=headers, data=request_data
            )

            self.logger.debug("Raw response from API: %s", response)

            if not isinstance(response, dict):
                raise ChatCompletionError("Невалидный ответ от API")

            if "error" in response:
                raise ChatCompletionError(response["error"])

            result_data = response.get("result", {})

            if not all(
                key in result_data for key in ["alternatives", "usage", "modelVersion"]
            ):
                self.logger.error("Invalid response structure: %s", response)
                raise ChatCompletionError("Неверная структура ответа от API")

            return ChatResponse(success=True, result=Result(**result_data))

        except Exception as e:
            self.logger.error("Ошибка при запросе к API Yandex: %s", str(e))
            raise ChatCompletionError(str(e))
