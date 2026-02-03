from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    """
    Обрабатывает /start и deep-link:
    /start
    /start job_123
    """

    text = (
        "👋 <b>Добро пожаловать!</b>\n\n"
        "Я публикую актуальные вакансии по Лазурному берегу "
        "и помогаю подготовить персонализированный отклик 🤖\n\n"
    )

    # проверяем, пришёл ли пользователь с вакансии
    if message.text and len(message.text.split()) > 1:
        payload = message.text.split()[1]

        if payload.startswith("job_"):
            job_id = payload.replace("job_", "")

            text += (
                f"Вы перешли по вакансии <b>№{job_id}</b>.\n"
                "Нажмите кнопку ниже, чтобы посмотреть подробности 👇"
            )

            await message.answer(text)
            return

    # обычный /start
    text += (
        "🔍 Вакансии публикуются в канале.\n"
        "Вы можете выбрать интересную и откликнуться через бота."
    )

    await message.answer(text)
