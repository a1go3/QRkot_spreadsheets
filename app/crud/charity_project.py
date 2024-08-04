from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """Расширяет базовый метод для CRUD операций."""

    @staticmethod
    async def get_charity_project_id_by_name(
        charity_project_name: str, session: AsyncSession
    ) -> Optional[int]:
        """Получение id проекта по его названию."""
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return charity_project_id.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
