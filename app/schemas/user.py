from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Pydantic схема для пользователя."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Pydantic схема для создания пользователя."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Pydantic схема для обновления пользователя."""

    pass
