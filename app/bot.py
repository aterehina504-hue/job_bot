import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from aiohttp import web

from app.config import AZUR_JOB_BOT_TOKEN
from app.handlers import start, details, jobs, apply

# =========================
# TELEGRAM BOT
# =========================
async def start_bot():
    bot = Bot(
        token=AZUR_JOB_BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(details.router)
    dp.include_router(jobs.router)
    dp.include_router(apply.router)

    print("🤖 Bot started")

    # 🔥 ЗАПУСКАЕМ ФОНОВЫЙ СБОР
    from app.services.job_collector import job_collector_loop
    asyncio.create_task(job_collector_loop(bot))

    await dp.start_polling(bot)

# =========================
# WEB SERVER (для Render)
# =========================
async def healthcheck(request):
    return web.Response(text="OK")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", healthcheck)

    port = int(os.getenv("PORT", "10000"))

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"🌐 Web server started on port {port}")

# =========================
# MAIN
# =========================
async def main():
    # 1️⃣ сначала открываем порт (Render!)
    await start_web_server()

    # 2️⃣ потом запускаем бота в фоне
    asyncio.create_task(start_bot())

    # 3️⃣ держим процесс живым
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
