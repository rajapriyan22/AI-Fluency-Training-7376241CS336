"""
Configuration module for the Day 1 Assessment project.
Configures Groq client via OpenAI-compatible SDK and loads environment variables.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load local .env file if present
load_dotenv()

# Groq API configuration
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model configuration (default to llama-3.3-70b-versatile or MODEL env var)
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. Please set it in your environment or local .env file."
    )

# Initialize OpenAI-compatible Groq client
client = OpenAI(
    base_url=GROQ_BASE_URL,
    api_key=GROQ_API_KEY,
)

# Test questions for the assessment
QUESTIONS = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students.",
]
