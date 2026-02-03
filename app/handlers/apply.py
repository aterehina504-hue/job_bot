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
        provider_token="",  # ⚠️ для Stars всегда пусто
        currency="XTR",     # ⭐ Telegram Stars
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
