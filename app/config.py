import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
AZUR_JOB_BOT_TOKEN = os.getenv("AZUR_JOB_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

TG_API_ID = int(os.getenv("TG_API_ID", "0"))
TG_API_HASH = os.getenv("TG_API_HASH")
