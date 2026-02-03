import asyncio

from aiogram import Bot

from app.services.parser import collect_raw_jobs
from app.services.job_pipeline import process_raw_job_and_publish

async def job_collector_loop(bot):
    print("🌀 Job collector loop running")

    me = await bot.get_me()
    bot_username = me.username
    print(f"🤖 Bot username: @{bot_username}")

    # 🔴 ТЕСТОВАЯ ВАКАНСИЯ (ПОКА ОСТАВЬ)
    await process_raw_job_and_publish(
        bot,
        "Официант в Каннах, ресторан, опыт приветствуется, контакт WhatsApp +33 6 00 00 00 00",
        bot_username
    )

    while True:
        try:
            raw_jobs = await collect_raw_jobs()
            print(f"📥 Raw jobs collected: {len(raw_jobs)}")

            for raw in raw_jobs:
                await process_raw_job_and_publish(
                    bot,
                    raw["text"],
                    bot_username
                )

        except Exception as e:
            print(f"❌ Job collector error: {e}")

        await asyncio.sleep(1800)
