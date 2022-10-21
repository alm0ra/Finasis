from os import getenv

DEBUG_MODE = getenv("DEBUG_MODE", "true")
PROXY_IP = getenv("PROXY_IP", None)
PROXY_PORT = getenv("PROXY_PORT", None)
