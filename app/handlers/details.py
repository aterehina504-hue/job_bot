from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.db.database import AsyncSessionLocal
from app.services.jobs import get_job_by_id
from app.keyboards.inline import job_details_keyboard

router = Router()


@router.callback_query(F.data.startswith("details:"))
async def job_details_handler(callback: CallbackQuery):
    job_id = int(callback.data.split(":")[1])

    async with AsyncSessionLocal() as session:
        job = await get_job_by_id(session, job_id)

    if not job:
        await callback.answer("Вакансия не найдена или больше неактуальна", show_alert=True)
        return

    text = (
        f"<b>{job.title}</b>\n\n"
        f"📍 <b>Город:</b> {job.city}\n"
        f"🕒 <b>Тип:</b> {job.job_type or '—'}\n"
        f"💶 <b>Зарплата:</b> {job.salary or '—'}\n\n"
        f"{job.full_description}\n\n"
        f"📲 <b>Контакт:</b> {job.contact or 'через бота'}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=job_details_keyboard(job.id)
    )

    await callback.answer()
