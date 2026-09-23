import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Reconfigure stdout to UTF-8 on Windows to handle symbols like ₹ without encoding errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

if not GROQ_API_KEY or GROQ_API_KEY == "your_key_here":
    raise ValueError("GROQ_API_KEY is missing or invalid in .env file. Please configure a valid Groq API key.")

# Groq OpenAI-compatible client setup
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# Mock Product Database Disclaimer
MOCK_DATABASE_DISCLAIMER = (
    "DISCLAIMER: This is a MOCK product database for demonstration purposes "
    "and does NOT represent live market prices or real-world product availability."
)

# Fictional Product Information
PRODUCTS = {
    "Nova X1": {
        "price": 18000,
        "ram": 8,
        "storage": 128,
        "battery": 5000,
        "rating": 4.2
    },
    "PixelMax P2": {
        "price": 24000,
        "ram": 8,
        "storage": 256,
        "battery": 5000,
        "rating": 4.5
    },
    "Turbo Z3": {
        "price": 28000,
        "ram": 12,
        "storage": 256,
        "battery": 6000,
        "rating": 4.4
    },
    "Lite M1": {
        "price": 15000,
        "ram": 6,
        "storage": 128,
        "battery": 5000,
        "rating": 4.0
    }
}
