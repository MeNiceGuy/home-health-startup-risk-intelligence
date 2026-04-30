import os

FREE_MODE = os.getenv("FREE_MODE", "true").lower() == "true"
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
APP_SECRET = os.getenv("APP_SECRET", "dev-secret-change-this")


