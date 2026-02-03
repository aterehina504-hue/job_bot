from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.services.ai import generate_application_text
from app.services.jobs import get_job_by_id

class ApplyForm(StatesGroup):
    experience = State()
    languages = State()
    availability = State()
    extra = State()

from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from app.db.database import AsyncSessionLocal
from app.db.models import UserPayment

router = Router()

PRICE_STARS = 50  # цена за 1 отклик


@router.callback_query(F.data.startswith("apply:"))
async def apply_handler(callback: CallbackQuery):
    job_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    async with AsyncSessionLocal() as session:
        payment = UserPayment(
            user_id=user_id,
            job_id=job_id,
            is_used=False
        )
        session.add(payment)
        await session.commit()
        await session.refresh(payment)

    await callback.message.answer_invoice(
        title="Персонализированный отклик",
        description=(
            "Я помогу составить персональный отклик:\n"
            "• под конкретную вакансию\n"
            "• на французском или английском\n"
            "• готовый к отправке"
        ),
        payload=str(payment.id),
        provider_token="",  
        currency="XTR",     
        prices=[
            LabeledPrice(
                label="1 отклик",
                amount=PRICE_STARS
            )
        ]
    )

    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment_handler(message: Message, state: FSMContext):
    payment_id = int(message.successful_payment.invoice_payload)

    async with AsyncSessionLocal() as session:
        payment = await session.get(UserPayment, payment_id)
        payment.is_used = True
        await session.commit()

    await state.update_data(job_id=payment.job_id)

    await message.answer(
        "Отлично! Начнём 👇\n\n"
        "1️⃣ Есть ли у вас опыт в этой сфере?"
    )
    await state.set_state(ApplyForm.experience)

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

@router.message(ApplyForm.extra)
async def finish_application(message: Message, state: FSMContext):
    data = await state.update_data(extra=message.text)
    job_id = data["job_id"]

    async with AsyncSessionLocal() as session:
        job = await get_job_by_id(session, job_id)

    await message.answer("🤖 Готовлю персонализированный отклик...")

    text = await generate_application_text(
        job_title=job.title,
        city=job.city,
        job_description=job.full_description,
        answers=data
    )

    await message.answer(
        "✅ Готово! Вот текст для отклика:\n\n"
        f"<b>{text}</b>\n\n"
        "Вы можете скопировать его и отправить работодателю 💼"
    )

    await state.clear()
