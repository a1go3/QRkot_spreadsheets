from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import Donation


class DonationCRUD(CRUDBase):
    """Расширяет базовый метод для CRUD операций."""

    @staticmethod
    async def all_current_user_donations_from_db(
        user, session
    ) -> list[Donation]:
        """Возвращает все пожертвования пользователя."""
        current_user_donations_from_db = await session.scalars(
            select(Donation).where(Donation.user_id == user.id)
        )
        return current_user_donations_from_db.all()


donation_crud = DonationCRUD(Donation)
