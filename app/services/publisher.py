from aiogram import Bot

from app.config import CHANNEL_ID
from app.keyboards.inline import channel_job_keyboard


async def publish_job_to_channel(
    bot: Bot,
    job,
    bot_username: str
):
    """
    Публикует вакансию в Telegram-канал
    """

    text = (
        f"💼 <b>{job.title}</b>\n"
        f"📍 {job.city}\n"
        f"🕒 {job.job_type or '—'}\n"
        f"💶 {job.salary or '—'}\n\n"
        f"{job.short_description}"
    )

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        reply_markup=channel_job_keyboard(bot_username, job.id)
    )
