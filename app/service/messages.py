from dataclasses import dataclass


@dataclass
class AppMessages:
    APP_TITLE: str = "Фонд QRKot."
    APP_DESCRIPTION: str = "Благотворительный фонд."
    PROJECT_EXISTS: str = "Проект с таким именем уже существует!"
    PROJECT_NOT_FOUND: str = "Проект с таким идентификатором не найден."
    CLOSE_PROJECT: str = "Нельзя редактировать закрытый проект."
    PROJECT_INVESTED: str = (
        "В проект были внесены средства, не подлежит удалению!"
    )
    PROJECT_UPDATE_FAILED: str = (
        "Нельзя установить значение full_amount меньше уже вложенной суммы."
    )
    PROJECT_NAME_FIELD_EMPTY: str = "Название проекта не может быть пустым!"
    USER_NAME_FIELD_EMPTY: str = "Имя пользователя не может быть пустым!"
    PASSWORD_FIELD_MIN: str = "Пароль должен содержать не менее 3 символов."
    PASSWORD_FIELD_EMAIL: str = (
        "Пароль не должен содержать адрес электронной почты."
    )
    USER_REGISTERED: str = "Пользователь зарегистрирован."
    DATABASE_URL: str = "sqlite+aiosqlite:///./cat_charity_find.db"
    DATABASE_NAME: str = ""
    SECRET_KEY: str = "secret"


@dataclass
class AppExamples:
    PROJECT_NAME: str = "На еду котам."
    PROJECT_DESCRIPTION: str = "Проект для кота, который хочет купить еду."
    PROJECT_ANOTHER_NAME: str = "На игрушки котам."
    PROJECT_ANOTHER_DESCRIPTION: str = (
        "Проект для кота, который хочет купить игрушки."
    )
    DONATION_COMMENT: str = "Пожертвование всякие цели."
