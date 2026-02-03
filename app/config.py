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
