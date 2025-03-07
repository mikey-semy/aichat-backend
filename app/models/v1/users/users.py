"""
Модуль, содержащий модели данных для работы с пользователями.

Этот модуль определяет следующие модели SQLAlchemy:
- UserModel: представляет пользователя в системе.

Модель наследуется от базового класса BaseModel и определяет
соответствующие поля и отношения между таблицами базы данных.

Модель использует типизированные аннотации Mapped для определения полей,
что обеспечивает улучшенную поддержку статической типизации.

Этот модуль предназначен для использования в сочетании с SQLAlchemy ORM
для выполнения операций с базой данных, связанных с пользователями.
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel
from app.models.v1.users.settings import UserSettingsModel


class UserModel(BaseModel):
    """
    Модель для представления пользователей.

    Attributes:
        name (str): Имя пользователя.
        email (str): Электронная почта пользователя.
        hashed_password (str): Хэшированный пароль пользователя.
        avatar (str): Ссылка на аватар пользователя.
        is_active (bool): Флаг активности пользователя.
        is_online (bool): Флаг онлайн-статуса пользователя.


    Relationships:
        feedbacks (list[FeedbackModel]): Список обратных связей пользователя (для менеджеров UserRole.MANAGER)
        video_lectures (list[VideoLectureModel]): Список видео лекций, созданных пользователем.
        tests (list[TestModel]): Список тестов, созданных пользователем.
        lectures (list[LectureModel]): Список лекций, созданных пользователем.
        posts (list[PostModel]): Список постов, созданных пользователем.
        chats (list[ChatModel]): Список чатов, созданных пользователем.
        aichat_usage (list[AIChatUsageModel]): Список использования AI пользователя.
    """

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    avatar: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_online: Mapped[bool] = mapped_column(default=False, nullable=False)

    settings: Mapped["UserSettingsModel"] = relationship(
        "UserSettingsModel", back_populates="user", uselist=False
    )