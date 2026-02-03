import asyncio

from app.db.database import AsyncSessionLocal
from app.db.models import Job


async def add_job():
    async with AsyncSessionLocal() as session:
        job = Job(
            title="Официант",
            category="Сервис и гостеприимство",
            city="Cannes",
            job_type="Сезонная",
            salary="от 1800 €",
            short_description="Ресторан в центре Канн, опыт приветствуется.",
            full_description=(
                "Требуется официант в ресторан.\n"
                "• Опыт от 6 месяцев\n"
                "• Французский язык — базовый\n"
                "• График сменный"
            ),
            contact="WhatsApp работодателя"
        )

        session.add(job)
        await session.commit()

        print(f"✅ Вакансия добавлена с ID: {job.id}")


if __name__ == "__main__":
    asyncio.run(add_job())
