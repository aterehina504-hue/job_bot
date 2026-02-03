import asyncio

from aiogram import Bot

from app.services.parser import collect_raw_jobs
from app.services.job_pipeline import process_raw_job_and_publish

async def job_collector_loop(bot):
    print("🌀 Job collector loop running")

    # 🔴 ТЕСТОВАЯ ВАКАНСИЯ (ОДИН РАЗ)
    await process_raw_job_and_publish(
        bot,
        "Официант в Каннах, ресторан, опыт приветствуется, жильё не предоставляется, контакт WhatsApp +33 6 00 00 00 00",
        bot.username
    )

    while True:
        ...
