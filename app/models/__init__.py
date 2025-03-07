"""
Пакет моделей данных.

Предоставляет единую точку доступа ко всем моделям приложения.
"""

from .v1.base import BaseModel
from .v1.users.users import UserModel
from .v1.users.settings import UserSettingsModel

__all__ = [
    "BaseModel",
    "UserModel",
    "UserSettingsModel"
]
