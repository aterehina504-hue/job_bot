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
