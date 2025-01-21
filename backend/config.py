import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GENAI_API_KEY  = os.getenv("GENAI_API_KEY")
CORS_ORIGIN = os.getenv("CORS_ORIGIN")  # Load the CORS origin from .env
