from sqlalchemy import Column, String

from app.service import AppNumbers

from .base import AppBase


class CharityProject(AppBase):
    """Модель для проектов."""

    name = Column(String(AppNumbers.MAX_LENGTH), unique=True, nullable=False)
    description = Column(String(length=AppNumbers.MIN_LENGTH), nullable=False)
