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
