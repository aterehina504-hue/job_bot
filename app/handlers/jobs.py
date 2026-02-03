from aiogram import Router
from aiogram.types import Message

from app.db.database import AsyncSessionLocal
from app.db.models import Job
from app.services.publisher import publish_job_to_channel

router = Router()


@router.message(lambda msg: msg.text == "/publish_test")
async def publish_test_job(message: Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            Job.__table__.select().limit(1)
        )
        job = result.first()

    if not job:
        await message.answer("❌ Нет вакансий в базе")
        return

    bot = message.bot
    bot_username = (await bot.get_me()).username

    await publish_job_to_channel(bot, job[0], bot_username)

    await message.answer("✅ Вакансия опубликована в канал")
