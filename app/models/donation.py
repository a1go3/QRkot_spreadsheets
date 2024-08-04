from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import AppBase


class Donation(AppBase):
    """Модель для пожертвований."""

    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
