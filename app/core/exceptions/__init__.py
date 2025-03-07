"""
Пакет исключений приложения.

Предоставляет централизованный доступ ко всем кастомным исключениям.

Example:
    >>> from app.core.exceptions import UserNotFoundError, UserExistsError
    >>> raise UserNotFoundError(user_id=42)
"""
from .handlers import (api_exception_handler, auth_exception_handler,
                               http_exception_handler,
                               internal_exception_handler,
                               validation_exception_handler,
                               websocket_exception_handler)
from .v1.base import BaseAPIException, DatabaseError, ValueNotFoundError
from .auth import (AuthenticationError, InvalidCredentialsError,
                    InvalidEmailFormatError, InvalidPasswordError,
                    WeakPasswordError, TokenExpiredError, TokenInvalidError, TokenMissingError)
from .v1.chat import ChatAuthError, ChatCompletionError

__all__ = [
    "api_exception_handler", 
    "auth_exception_handler",
    "http_exception_handler",
    "internal_exception_handler",
    "validation_exception_handler",
    "websocket_exception_handler",
    "BaseAPIException",
    "DatabaseError",
    "ValueNotFoundError",
    "TokenExpiredError",
    "TokenInvalidError",
    "TokenMissingError",
    "AuthenticationError",
    "InvalidCredentialsError",
    "ChatAuthError",
    "ChatCompletionError"
]
