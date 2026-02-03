from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def generate_application_text(
    job_title: str,
    city: str,
    job_description: str,
    answers: dict
) -> str:
    """
    Генерирует персонализированный текст отклика
    """

    prompt = f"""
Ты — помощник по поиску работы во Франции.
Сгенерируй КОРОТКИЙ и ПРОФЕССИОНАЛЬНЫЙ текст отклика.

Вакансия:
Должность: {job_title}
Город: {city}
Описание: {job_description}

Информация о кандидате:
Опыт: {answers.get("experience")}
Языки: {answers.get("languages")}
Доступность: {answers.get("availability")}
Дополнительно: {answers.get("extra")}

Требования к ответу:
- язык: французский
- стиль: вежливый, деловой
- 5–7 строк
- без эмодзи
- готов к отправке работодателю
"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()
