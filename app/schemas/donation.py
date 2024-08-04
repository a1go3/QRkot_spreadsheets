from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt
from pydantic.schema import Optional

from app.service import AppExamples


class DonationCreate(BaseModel):
    """Базовая Pydantic схема для создания пожертвований."""

    full_amount: PositiveInt
    comment: Optional[str] = Field(example=AppExamples.DONATION_COMMENT)


class DonationCreateDB(DonationCreate):
    """Pydantic схема для отображения пожертвования после создания."""

    full_amount: PositiveInt
    comment: Optional[str] = Field(example=AppExamples.DONATION_COMMENT)
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    """Pydantic схема для отображения списка пожертвований."""

    full_amount: PositiveInt
    comment: Optional[str] = Field(example=AppExamples.DONATION_COMMENT)
    id: int
    create_date: datetime
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
