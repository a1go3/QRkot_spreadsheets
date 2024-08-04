from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.invest import invest
from app.api.validators import AppValidators
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Endpoint для создания нового благотворительного проекта.
    Доступен только пользователям со статусом super_user."""
    await AppValidators.check_name_charity_project_duplicate(
        charity_project.name, session
    )
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    return await invest(new_charity_project, session)


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


@router.patch(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Endpoint для обновления данных в благотворительном проекте.
    Доступен только пользователям со статусом super_user."""
    await AppValidators.check_charity_project_exists(
        charity_project_id, session
    )
    charity_project = await AppValidators.check_charity_project_is_closed(
        charity_project_id, session
    )

    if obj_in.name is not None:
        await AppValidators.check_name_charity_project_duplicate(
            obj_in.name, session
        )

    await AppValidators.check_charity_project_full_amount(
        charity_project, obj_in, session
    )

    return await charity_project_crud.update(charity_project, obj_in, session)


@router.delete(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    charity_project_id: int, session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Endpoint для удаления благотворительных проектов.
    Удалять можно только проекты, в которые не было внесено средств.
    Доступен только пользователям со статусом super_user."""
    charity_project = await AppValidators.check_charity_project_exists(
        charity_project_id, session
    )
    return await AppValidators.check_charity_project_invested_amount_exists(
        charity_project, session
    )
