import asyncio

from aiogram import Bot

from app.services.parser import collect_raw_jobs
from app.services.job_pipeline import process_raw_job_and_publish


async def job_collector_loop(
    bot: Bot,
    interval: int = 1800  # 30 минут
):
    """
    Фоновый сбор вакансий:
    Telegram → ИИ → БД → Канал
    """
    bot_username = (await bot.get_me()).username

    print("🌀 Job collector started")

    while True:
        try:
            raw_jobs = await collect_raw_jobs()

            for raw in raw_jobs:
                await process_raw_job_and_publish(
                    bot=bot,
                    raw_text=raw["text"],
                    bot_username=bot_username
                )

        except Exception as e:
            print(f"❌ Job collector error: {e}")

        await asyncio.sleep(interval)
