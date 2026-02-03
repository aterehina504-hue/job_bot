import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.config import AZUR_JOB_BOT_TOKEN


async def main():
    bot = Bot(
        token=AZUR_JOB_BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()

    # handlers будем подключать на следующих шагах

    print("🤖 Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
