from typing import Optional

from sqlalchemy import func, select
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

    @staticmethod
    async def get_projects_by_completion_rate(session: AsyncSession):
        """Получение списка со всеми закрытыми проектами
        отсортированного по количеству времени, которое понадобилось на сбор
        средств, — от меньшего к большему"""
        db_objs = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested == True)
            .order_by(
                func.datediff(
                    CharityProject.close_date, CharityProject.create_date
                ).asc()
            )
        )

        return db_objs.all()


charity_project_crud = CRUDCharityProject(CharityProject)
