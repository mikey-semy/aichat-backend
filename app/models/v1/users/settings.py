"""
Модуль, содержащий модель настроек пользователя.

Модель предназначена для хранения пользовательских настроек,
включая предпочитаемую модель AI для использования в чате.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel
from app.schemas import ModelType
from app.models.v1 import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.v1.users import UserModel

class UserSettingsModel(BaseModel):
    """
    Модель для хранения настроек пользователя.

    Attributes:
        user_id (int): ID пользователя, которому принадлежат настройки.
        preferred_model (ModelType): Предпочитаемая модель AI.
        temperature (float): Настройка температуры для генерации.
        max_tokens (int): Максимальное количество токенов для генерации.

    Relationships:
        user (UserModel): Пользователь, которому принадлежат настройки.
    """

    __tablename__ = "user_settings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    preferred_model: Mapped[ModelType] = mapped_column(default=ModelType.LLAMA_70B)
    temperature: Mapped[float] = mapped_column(default=0.6)
    max_tokens: Mapped[int] = mapped_column(default=2000)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="settings")
