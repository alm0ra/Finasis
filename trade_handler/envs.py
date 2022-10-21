from os import getenv

DEBUG_MODE = getenv("DEBUG_MODE", "true")
PROXY_IP = getenv("PROXY_IP", None)
PROXY_PORT = getenv("PROXY_PORT", None)

TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID", None)
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN", None)
