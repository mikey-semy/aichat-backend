"""
Исключения для аутентификации и управления пользователями.

Базовый класс AuthenticationError наследуется от BaseAPIException
"""

from app.core.exceptions.v1.base import BaseAPIException


class AuthenticationError(BaseAPIException):
    """
    Ошибка аутентификации/авторизации
    """

    def __init__(self, message: str, extra: dict = None):
        super().__init__(
            status_code=401,
            detail=f"Ошибка авторизации: {message}",
            error_type="auth_error",
            extra=extra,
        )

class InvalidCredentialsError(AuthenticationError):
    """Неверные учетные данные"""

    def __init__(self):
        super().__init__(message="🔐 Неверный email или пароль")
