from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.service import AppMessages


class AppValidators:
    """Класс проверки валидности данных для CRUD запросов."""

    @staticmethod
    async def check_name_charity_project_duplicate(
        charity_project_name: str,
        session: AsyncSession,
    ) -> None:
        """Проверка наличия проекта с таким же именем в базе данных."""
        charity_project_id = (
            await charity_project_crud.get_charity_project_id_by_name(
                charity_project_name, session
            )
        )
        if charity_project_id is not None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST.value,
                detail=AppMessages.PROJECT_EXISTS,
            )

    @staticmethod
    async def check_charity_project_exists(
        charity_project_id: int, session: AsyncSession
    ) -> CharityProject:
        """Проверка наличия проекта с определенным идентификатором
        в базе данных"""
        charity_project = await charity_project_crud.get(
            charity_project_id,
            session,
        )
        if charity_project is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value,
                detail=AppMessages.PROJECT_NOT_FOUND,
            )
        return charity_project

    @staticmethod
    async def check_charity_project_is_closed(
        charity_project_id: int, session: AsyncSession
    ) -> CharityProject:
        """Проверка наличия закрытого проекта с определенным идентификатором
        в базе данных"""
        charity_project = await charity_project_crud.get(
            charity_project_id, session
        )
        if charity_project.fully_invested is True:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST.value,
                detail=AppMessages.CLOSE_PROJECT,
            )
        return charity_project

    @staticmethod
    async def check_charity_project_invested_amount_exists(
        charity_project: CharityProject, session: AsyncSession
    ) -> CharityProject:
        """Проверка наличия в проекте суммы вложения."""
        if charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST.value,
                detail=AppMessages.PROJECT_INVESTED,
            )
        return charity_project

    @staticmethod
    async def check_charity_project_full_amount(
        charity_project: CharityProject, obj_in, session: AsyncSession
    ) -> CharityProject:
        """Проверка, что при обновлении в проекте значения требуемой суммы
        новое значение не превышает сумму уже вложенного."""
        if obj_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST.value,
                detail=AppMessages.PROJECT_UPDATE_FAILED,
            )
        return charity_project
