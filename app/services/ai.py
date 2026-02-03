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

import json
from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def ai_filter_and_parse_job(raw_text: str) -> dict | None:
    """
    Фильтрует текст и возвращает структурированную вакансию на русском языке
    или None, если это не вакансия
    """

    prompt = f"""
Ты — HR-ассистент, специализирующийся на рынке труда Франции.

Твоя задача:
1. Определить, является ли текст вакансией.
2. Если НЕТ — ответь строго: NO
3. Если ДА — верни ТОЛЬКО валидный JSON (без пояснений).

Разрешённые сферы:
- рестораны
- отели
- недвижимость
- айти
- бьюти
- репетиторство и курсы
- водители
- уборка
- няни и сиделки
- разовые подработки
- строительство
- торговля
- онлайн продвижение

JSON-формат:
{{
  "title": "",
  "category": "",
  "city": "",
  "job_type": "",
  "salary": "",
  "short_description": "",
  "full_description": "",
  "contact": ""
}}

Правила:
- язык результата: русский
- если нет города или контакта — верни NO
- если сфера не из списка — верни NO
- short_description — 1–2 строки
- full_description — нормальный читабельный текст

Текст:
\"\"\"
{raw_text}
\"\"\"
"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    if content == "NO":
        return None

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None
