from datetime import datetime

from pydantic import BaseModel, Extra, Field, PositiveInt, validator
from pydantic.schema import Optional

from app.service import AppExamples, AppMessages, AppNumbers


class CharityProjectCreate(BaseModel):
    """Pydantic схема для создания проектов."""

    name: str = Field(
        min_length=AppNumbers.MIN_LENGTH,
        max_length=AppNumbers.MAX_LENGTH,
        example=AppExamples.PROJECT_NAME,
    )
    description: str = Field(
        min_length=AppNumbers.MIN_LENGTH,
        example=AppExamples.PROJECT_DESCRIPTION,
    )
    full_amount: PositiveInt

    @validator("name")
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(AppMessages.PROJECT_NAME_FIELD_EMPTY)
        return value


class CharityProjectUpdate(BaseModel):
    """Pydantic схема для обновления проектов."""

    name: Optional[str] = Field(
        min_length=AppNumbers.MIN_LENGTH,
        max_length=AppNumbers.MAX_LENGTH,
        example=AppExamples.PROJECT_ANOTHER_NAME,
    )
    description: Optional[str] = Field(
        min_length=AppNumbers.MIN_LENGTH,
        example=AppExamples.PROJECT_ANOTHER_DESCRIPTION,
    )
    full_amount: Optional[PositiveInt] = Field(
        default=AppNumbers.DEFAULT_LENGTH
    )

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    """Pydantic схема для отображения проектов."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
