from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charity_project import charity_project_crud
from app.schemas import CharityProjectDB
from app.service.google_api import (
    spreadsheets_create,
    set_user_permissions,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post(
    "/",
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
) -> list[CharityProjectDB]:
    """Endpoint для создания отчета в гугл таблицу.
    Доступен только пользователям со статусом super_user."""
    charity_projects = (
        await charity_project_crud.get_projects_by_completion_rate(session)
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid,
        charity_projects,
        wrapper_services,
    )

    return charity_projects
