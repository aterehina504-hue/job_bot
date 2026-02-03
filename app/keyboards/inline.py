from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def job_details_keyboard(job_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🤖 Откликнуться через бота",
                callback_data=f"apply:{job_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back"
            )
        ]
    ])

from app.config import AZUR_JOB_BOT_TOKEN  # не используется напрямую, просто для импорта


def channel_job_keyboard(bot_username: str, job_id: int):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🤖 Откликнуться через бота",
                url=f"https://t.me/AzurJobBot?start=job_{job_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ Подробнее о вакансии",
                callback_data=f"details:{job_id}"
            )
        ]
    ])

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.services.payments import PACKAGES

def packages_keyboard(job_id: int):
    buttons = []
    for code, p in PACKAGES.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{p['title']} — {p['price']} ⭐",
                callback_data=f"buy:{code}:{job_id}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
