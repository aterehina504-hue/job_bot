from aiogram import Bot

from app.db.database import AsyncSessionLocal
from app.services.ai import ai_filter_and_parse_job
from app.services.jobs import save_job
from app.services.publisher import publish_job_to_channel


async def process_raw_job_and_publish(
    bot: Bot,
    raw_text: str,
    bot_username: str
):
    """
    Полный цикл:
    raw text → ИИ → БД → публикация
    """

    # 1️⃣ ИИ-фильтр
    data = await ai_filter_and_parse_job(raw_text)
    if not data:
        return

    # 2️⃣ Сохранение + анти-дубли
    async with AsyncSessionLocal() as session:
        job = await save_job(session, data)

    if not job:
        return  # дубль

    # 3️⃣ Публикация в канал
    await publish_job_to_channel(bot, job, bot_username)
