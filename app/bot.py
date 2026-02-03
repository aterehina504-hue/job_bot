import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.config import AZUR_JOB_BOT_TOKEN
from app.handlers import start, details, jobs


async def main():
    bot = Bot(
        token=AZUR_JOB_BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()

    # ✅ ВСЕ routers подключаются ТОЛЬКО здесь
    dp.include_router(start.router)
    dp.include_router(details.router)
    dp.include_router(jobs.router)

    print("🤖 Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
