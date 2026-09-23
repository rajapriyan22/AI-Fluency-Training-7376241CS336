import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_environment():
    print("==================================================")
    print("ASSESSMENT DAY 2 — ENVIRONMENT & SETUP CHECK")
    print("==================================================")

    # 1. Python Version Check
    py_version = sys.version.split()[0]
    print(f"[✓] Python Version: {py_version}")

    # 2. Package Check: openai
    try:
        import openai
        print(f"[✓] Package 'openai' is installed (v{openai.__version__})")
    except ImportError:
        print("[✗] ERROR: Package 'openai' is NOT installed.")
        sys.exit(1)

    # 3. Package Check: python-dotenv
    try:
        import dotenv
        print(f"[✓] Package 'python-dotenv' is installed")
    except ImportError:
        print("[✗] ERROR: Package 'python-dotenv' is NOT installed.")
        sys.exit(1)

    # 4. Config & API Key Check
    try:
        from config import GROQ_API_KEY, MODEL, client
        if not GROQ_API_KEY:
            print("[✗] ERROR: GROQ_API_KEY not found in environment.")
            sys.exit(1)
        
        masked_key = GROQ_API_KEY[:4] + "..." + GROQ_API_KEY[-4:] if len(GROQ_API_KEY) > 8 else "***"
        print(f"[✓] GROQ_API_KEY loaded: {masked_key}")
        print(f"[✓] Configured Model: {MODEL}")

        # 5. Groq API Connection Test
        print("\nTesting Groq API connection...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "Respond with 'OK' to confirm API connection."}],
            max_tokens=20
        )
        reply = response.choices[0].message.content.strip()
        print(f"[✓] Groq API Response: '{reply}'")
        print("\n[SUCCESS] Setup check passed! All dependencies and API connections are working.")

    except Exception as e:
        print(f"[✗] ERROR during setup check: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_environment()
