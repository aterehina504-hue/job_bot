from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    LabeledPrice,
    PreCheckoutQuery
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.db.database import AsyncSessionLocal
from app.db.models import UserBalance
from app.services.payments import PACKAGES
from app.services.ai import generate_application_text
from app.services.jobs import get_job_by_id
from app.keyboards.inline import packages_keyboard

router = Router()


# =========================
# FSM STATES
# =========================
class ApplyForm(StatesGroup):
    experience = State()
    languages = State()
    availability = State()
    extra = State()


# =========================
# ENTRY: APPLY BUTTON (SCREEN 1)
# =========================
@router.callback_query(F.data.startswith("apply:"))
async def apply_entry(callback: CallbackQuery):
    job_id = int(callback.data.split(":")[1])

    text = (
        "💼 <b>Персональный отклик от ИИ</b>\n\n"
        "📌 Что важно по этой вакансии:\n"
        "• персональные отклики получают ответ чаще\n"
        "• опыт важнее идеального французского\n"
        "• без отклика резюме часто игнорируют\n\n"
        "👇 Выберите формат помощи:"
    )

    await callback.message.answer(
        text=text,
        reply_markup=packages_keyboard(job_id)
    )
    await callback.answer()


# =========================
# BUY PACKAGE
# =========================
@router.callback_query(F.data.startswith("buy:"))
async def buy_package(callback: CallbackQuery):
    _, code, job_id = callback.data.split(":")
    package = PACKAGES[code]

    await callback.message.answer_invoice(
        title=f"Пакет: {package['title']}",
        description="Персональные ИИ-отклики для поиска работы",
        payload=f"{code}:{job_id}",
        provider_token="",  # для Stars всегда пусто
        currency="XTR",
        prices=[
            LabeledPrice(
                label=package["title"],
                amount=package["price"]
            )
        ]
    )
    await callback.answer()


# =========================
# PRE-CHECKOUT (REQUIRED)
# =========================
@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


# =========================
# PAYMENT SUCCESS (SCREEN 2)
# =========================
@router.message(F.successful_payment)
async def payment_success(message: Message, state: FSMContext):
    code, job_id = message.successful_payment.invoice_payload.split(":")
    package = PACKAGES[code]
    user_id = message.from_user.id

    async with AsyncSessionLocal() as session:
        balance = await session.get(UserBalance, user_id)
        if not balance:
            balance = UserBalance(user_id=user_id, credits=0)
            session.add(balance)

        balance.credits += package["credits"]
        await session.commit()

    await state.update_data(job_id=int(job_id))

    await message.answer(
        "✅ <b>Оплата прошла успешно!</b>\n\n"
        f"Ваш баланс: <b>{balance.credits}</b> откликов\n\n"
        "🤖 Сейчас я:\n"
        "• задам несколько вопросов\n"
        "• учту требования вакансии\n"
        "• подготовлю текст, готовый к отправке\n\n"
        "Начнём 👇\n"
        "1️⃣ Есть ли у вас опыт в этой сфере?"
    )

    await state.set_state(ApplyForm.experience)


# =========================
# FSM QUESTIONS
# =========================
@router.message(ApplyForm.experience)
async def experience_step(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("2️⃣ Какими языками вы владеете?")
    await state.set_state(ApplyForm.languages)


@router.message(ApplyForm.languages)
async def languages_step(message: Message, state: FSMContext):
    await state.update_data(languages=message.text)
    await message.answer("3️⃣ Когда вы готовы приступить к работе?")
    await state.set_state(ApplyForm.availability)


@router.message(ApplyForm.availability)
async def availability_step(message: Message, state: FSMContext):
    await state.update_data(availability=message.text)
    await message.answer(
        "4️⃣ Хотите добавить что-то ещё? (или напишите «нет»)"
    )
    await state.set_state(ApplyForm.extra)

# =========================
# FINAL: AI GENERATION (SCREEN 3 + 4)
# =========================
@router.message(ApplyForm.extra)
async def finish_application(message: Message, state: FSMContext):
    data = await state.update_data(extra=message.text)
    job_id = data["job_id"]

    async with AsyncSessionLocal() as session:
        job = await get_job_by_id(session, job_id)

    await message.answer(
        "⏳ Анализирую вакансию и ваши ответы…\n"
        "Обычно это занимает 10–15 секунд"
    )

    text = await generate_application_text(
        job_title=job.title,
        city=job.city,
        job_description=job.full_description,
        answers=data
    )

    await message.answer(
        "✅ <b>Готово!</b>\n\n"
        "Вот персональный текст отклика 👇\n\n"
        f"<i>{text}</i>\n\n"
        "💡 Совет:\n"
        "Если не ответят за 2–3 дня — можно написать повторно."
    )

    await state.clear()
