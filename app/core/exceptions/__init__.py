"""
Пакет исключений приложения.

Предоставляет централизованный доступ ко всем кастомным исключениям.

Example:
    >>> from app.core.exceptions import UserNotFoundError, UserExistsError
    >>> raise UserNotFoundError(user_id=42)
"""

from .v1.base import BaseAPIException, DatabaseError, ValueNotFoundError
from .v1.security import (TokenExpiredError, TokenInvalidError,
                               TokenMissingError)
from .v1.auth import AuthenticationError, InvalidCredentialsError
from .v1.chat import ChatAuthError, ChatCompletionError
__all__ = [
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
