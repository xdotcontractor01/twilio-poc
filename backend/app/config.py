import os

from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID: str = os.getenv("ACCOUNT_SID", "")
AUTH_TOKEN: str = os.getenv("AUTH_TOKEN", "")
TWILIO_NUMBER: str = os.getenv("TWILIO_NUMBER", "")
TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "")
