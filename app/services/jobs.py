from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Job


async def get_job_by_id(
    session: AsyncSession,
    job_id: int
) -> Job | None:
    result = await session.execute(
        select(Job).where(Job.id == job_id, Job.is_active == True)
    )
    return result.scalar_one_or_none()

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Job


async def job_exists(
    session: AsyncSession,
    title: str,
    city: str,
    contact: str
) -> bool:
    """
    Проверяет, есть ли уже такая вакансия
    """
    result = await session.execute(
        select(Job).where(
            and_(
                Job.title == title,
                Job.city == city,
                Job.contact == contact,
                Job.is_active == True
            )
        )
    )
    return result.scalar_one_or_none() is not None
