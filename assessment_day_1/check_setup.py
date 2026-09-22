"""
Script to verify Python environment, Groq API connection, and model response.
"""
import sys
from config import client, MODEL, GROQ_BASE_URL


def check_environment():
    print("=== CHECK SETUP: DAY 1 ASSESSMENT ===")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Groq Base URL: {GROQ_BASE_URL}")
    print(f"Configured Model: {MODEL}")

    try:
        print("\nTesting connection to Groq API...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Respond with 'Groq API connected successfully!'"}
            ],
            max_tokens=30,
        )
        content = response.choices[0].message.content.strip()
        print(f"\nModel Response:\n{content}")
        print("\nSUCCESS: Groq API connection verified successfully!")
        return True
    except Exception as e:
        print(f"\nERROR: Failed to connect to Groq API: {e}")
        return False


if __name__ == "__main__":
    success = check_environment()
    if not success:
        sys.exit(1)
