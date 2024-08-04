from datetime import datetime
from typing import Union

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import CharityProject, Donation


async def invest(
    model_in: Union[Donation, CharityProject],
    session: AsyncSession = Depends(get_async_session),
) -> Donation:
    """Процесс инвестирования."""
    object_in = model_in
    objects_from_db = await get_open_entities(model_in, session)
    for object_db in objects_from_db:
        object_in = (
            model_in if isinstance(model_in, CharityProject) else object_db
        )
        object_db = model_in
        how_cost = object_db.full_amount - object_db.invested_amount
        remains = object_in.full_amount - object_in.invested_amount
        if remains < how_cost:
            object_db.invested_amount += remains
            object_in.invested_amount = object_in.full_amount
            object_in.fully_invested = True
            object_in.close_date = datetime.utcnow()
        else:
            object_db.fully_invested = True
            object_db.close_date = datetime.utcnow()
            object_db.invested_amount = object_db.full_amount
            object_in.invested_amount += how_cost
            if remains == how_cost:
                object_in.fully_invested = True
                object_in.close_date = datetime.utcnow()
            break
    await session.commit()
    await session.refresh(object_in)
    return object_in


async def get_open_entities(
    model_in: Union[Donation, CharityProject],
    session: AsyncSession,
):
    """Вспомогательная функция для процесса инвестирования.
    В зависимости от полученной модели возвращает
    либо открытые проекты, либо неизрасходованные пожертвования,
    сортируя по дате создания"""
    model = (
        Donation if isinstance(model_in, CharityProject) else CharityProject
    )

    objects_from_db = await session.scalars(
        select(model)
        .where(model.fully_invested == 0)
        .order_by(model.create_date)
    )

    return objects_from_db.all()
