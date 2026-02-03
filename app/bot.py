import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from aiohttp import web

from app.config import AZUR_JOB_BOT_TOKEN
from app.handlers import start, details, jobs


# ---------- WEB SERVER ----------
async def healthcheck(request):
    return web.Response(text="OK")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", healthcheck)

    port = int(os.getenv("PORT", 10000))

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"🌐 Web server started on port {port}")


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


# ---------- MAIN ----------
async def main():
    await asyncio.gather(
        start_bot(),
        start_web_server()
    )


if __name__ == "__main__":
    asyncio.run(main())
