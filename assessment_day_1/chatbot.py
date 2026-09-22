"""
System 1 — Plain Chatbot
Sends questions directly to Groq LLM without private data access or tools.
Demonstrates LLM behavior and limitations on private domain questions.
"""
import sys
import io

# Ensure UTF-8 output encoding for Windows console compatibility
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from config import client, MODEL, QUESTIONS


def run_chatbot():
    print("==================================================")
    print("SYSTEM 1: PLAIN CHATBOT")
    print("==================================================")
    print(f"Provider: Groq | Model: {MODEL}")
    print("Context: No private data provided. No tools enabled.\n")

    for i, question in enumerate(QUESTIONS, 1):
        print(f"--- Question {i} ---")
        print(f"Q: {question}")
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful college assistant. Answer questions concisely. "
                            "If you do not have specific private data, answer truthfully based on your general knowledge or state that you lack private database access."
                        ),
                    },
                    {"role": "user", "content": question},
                ],
                temperature=0.2,
                max_tokens=150,
            )
            answer = response.choices[0].message.content.strip()
            print(f"A: {answer}\n")
        except Exception as e:
            print(f"A: [Error calling Groq API: {e}]\n")


if __name__ == "__main__":
    run_chatbot()
