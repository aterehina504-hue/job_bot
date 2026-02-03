from telethon import TelegramClient
from telethon.tl.types import Message

from app.config import TG_API_ID, TG_API_HASH


# ⚠️ публичные каналы, без @
SOURCE_CHANNELS = [
    "cotedazurjobs",
    "jobsfranceru",
    "nicecannesjobs",
]


async def collect_raw_jobs(limit: int = 50) -> list[dict]:
    """
    Собирает сырые тексты вакансий из Telegram-каналов
    """
    client = TelegramClient(
        "job_collector_session",
        TG_API_ID,
        TG_API_HASH
    )

    raw_jobs = []

    async with client:
        for channel in SOURCE_CHANNELS:
            async for message in client.iter_messages(channel, limit=limit):
                if not isinstance(message, Message):
                    continue

                if not message.text:
                    continue

                raw_jobs.append({
                    "source": f"telegram:{channel}",
                    "text": message.text,
                    "message_id": message.id
                })

    return raw_jobs
