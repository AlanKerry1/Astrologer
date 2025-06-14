import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")