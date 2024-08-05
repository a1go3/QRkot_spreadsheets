from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charity_project import charity_project_crud
from app.schemas import CharityProjectDB


router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    # «Обёртка»
    # wrapper_services: Aiogoogle = Depends(get_service),
) -> list[CharityProjectDB]:
    """Endpoint для получения списка всех благотворительных проектов.
    Доступен для любого (в том числе неавторизированного) пользователя."""
    return await charity_project_crud.get_projects_by_completion_rate(session)


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[CharityProjectDB]:
    """Endpoint для получения списка всех благотворительных проектов.
    Доступен для любого (в том числе неавторизированного) пользователя."""
    return await charity_project_crud.get_all(session)
