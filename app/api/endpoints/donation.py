from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.invest import invest
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationCreateDB, DonationDB

router = APIRouter()


@router.post(
    "/", response_model=DonationCreateDB, response_model_exclude_none=True
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> DonationCreateDB:
    """Endpoint для внесения пожертвования.
    Доступен только зарегистрированному пользователю."""
    new_donation = await donation_crud.create(donation, session, user)
    return await invest(new_donation, session)


@router.get(
    "/",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[DonationDB]:
    """Endpoint для просмотра всех пожертвований.
    Доступен только пользователям со статусом super_user."""
    return await donation_crud.get_all(session)


@router.get(
    "/my",
    response_model=list[DonationCreateDB],
    response_model_exclude_none=True,
)
async def get_all_current_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> list[DonationCreateDB]:
    """Endpoint для просмотра пользователем списка своих пожертвований.
    Доступен только зарегистрированному пользователю."""
    return await donation_crud.all_current_user_donations_from_db(
        user, session
    )
