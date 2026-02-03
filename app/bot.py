from app.db.database import engine, Base
import app.db.models 

import asyncio
import os

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.config import AZUR_JOB_BOT_TOKEN
from app.handlers import start, details, jobs, apply


WEBHOOK_PATH = "/webhook"
BASE_URL = os.getenv("WEBHOOK_BASE_URL").rstrip("/")
WEBHOOK_URL = BASE_URL + WEBHOOK_PATH


# =========================
# BOT & DISPATCHER
# =========================
bot = Bot(
    token=AZUR_JOB_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(details.router)
dp.include_router(jobs.router)
dp.include_router(apply.router)

async def init_db():
    print("🧪 Tables before:", Base.metadata.tables.keys())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("🗄️ Database initialized")

# =========================
# WEB SERVER
# =========================
async def healthcheck(request):
    return web.Response(text="OK")

from app.db.database import engine
from app.db.models import Base

async def on_startup(app):
    await init_db()

    await bot.set_webhook(WEBHOOK_URL)
    print(f"🔗 Webhook set to {WEBHOOK_URL}")

    from app.services.job_collector import job_collector_loop
    asyncio.create_task(job_collector_loop(bot))
    print("🌀 Job collector started")

async def on_shutdown(app):
    await bot.delete_webhook()


def create_app():
    app = web.Application()

    # healthcheck — ОБЯЗАТЕЛЬНО
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
    print(f"🌐 Starting web server on port {port}")
    web.run_app(create_app(), host="0.0.0.0", port=port)
