import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from aiohttp import web

from app.config import AZUR_JOB_BOT_TOKEN
from app.handlers import start, details, jobs


# ---------- TELEGRAM BOT ----------
async def start_bot():
    bot = Bot(
        token=AZUR_JOB_BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(details.router)
    dp.include_router(jobs.router)

    print("🤖 Bot started")
    await dp.start_polling(bot)


# ---------- WEB SERVER ----------
async def healthcheck(request):
    return web.Response(text="OK")


async def create_web_app():
    app = web.Application()
    app.router.add_get("/", healthcheck)
    return app


async def main():
    # 1️⃣ СНАЧАЛА поднимаем web-сервер
    port = int(os.getenv("PORT", "10000"))

    app = await create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"🌐 Web server started on port {port}")

    # 2️⃣ ПОТОМ запускаем бота в фоне
    asyncio.create_task(start_bot())

    # 3️⃣ держим процесс живым
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
