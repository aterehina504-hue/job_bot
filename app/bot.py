import asyncio
import os

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.config import AZUR_JOB_BOT_TOKEN
from app.handlers import start, details, jobs, apply


WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL") + WEBHOOK_PATH


# =========================
# BOT & DISPATCHER
# =========================
bot = Bot(
    token=AZUR_JOB_BOT_TOKEN,
    parse_mode=ParseMode.HTML
)

dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(details.router)
dp.include_router(jobs.router)
dp.include_router(apply.router)


# =========================
# WEB SERVER
# =========================
async def healthcheck(request):
    return web.Response(text="OK")


async def on_startup(app):
    # ставим webhook
    await bot.set_webhook(WEBHOOK_URL)
    print(f"🔗 Webhook set to {WEBHOOK_URL}")

    # запускаем job collector
    from app.services.job_collector import job_collector_loop
    asyncio.create_task(job_collector_loop(bot))


async def on_shutdown(app):
    await bot.delete_webhook()


def create_app():
    app = web.Application()

    # healthcheck (для Render)
    app.router.add_get("/", healthcheck)

    # webhook endpoint
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    ).register(app, path=WEBHOOK_PATH)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    setup_application(app, dp, bot=bot)
    return app


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    web.run_app(create_app(), host="0.0.0.0", port=port)
