from ..base import BaseInputSchema

class UserCredentialsSchema(BaseInputSchema):
    """
    Схема учетных данных пользователя.


    Attributes:
        id (int): Идентификатор пользователя.
        name (str): Имя пользователя (необязательно).
        email (str): Email пользователя.
        hashed_password (str | None): Хешированный пароль пользователя.
        is_active (bool): Флаг активности пользователя.
    """

    id: int | None = None
    name: str | None = None
    email: str
    hashed_password: str | None = None
    is_active: bool = True