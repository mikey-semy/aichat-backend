"""
Пакет исключений приложения.

Предоставляет централизованный доступ ко всем кастомным исключениям.

Example:
    >>> from app.core.exceptions import UserNotFoundError, UserExistsError
    >>> raise UserNotFoundError(user_id=42)
"""

from .v1.base import BaseAPIException, DatabaseError, ValueNotFoundError
from .v1.auth import AuthenticationError
__all__ = [
    "BaseAPIException",
    "DatabaseError",
    "ValueNotFoundError",
    "AuthenticationError",
]
