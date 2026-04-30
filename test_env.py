import os
from dotenv import load_dotenv

load_dotenv()
print("STRIPE KEY:", os.getenv("STRIPE_SECRET_KEY"))


