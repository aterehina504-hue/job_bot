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

async def save_job(
    session: AsyncSession,
    data: dict
) -> Job | None:
    """
    Сохраняет вакансию в БД, если она не дубль
    """
    if await job_exists(
        session,
        title=data["title"],
        city=data["city"],
        contact=data["contact"]
    ):
        return None

    job = Job(
        title=data["title"],
        category=data["category"],
        city=data["city"],
        job_type=data.get("job_type"),
        salary=data.get("salary"),
        short_description=data["short_description"],
        full_description=data["full_description"],
        contact=data["contact"],
    )

    session.add(job)
    await session.commit()
    await session.refresh(job)

    return job

