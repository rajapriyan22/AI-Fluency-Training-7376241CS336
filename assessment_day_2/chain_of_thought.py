import sys
import json
from config import client, MODEL, PRODUCTS, MOCK_DATABASE_DISCLAIMER

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_chain_of_thought(question: str, context: str = None) -> str:
    """
    Executes a Chain-of-Thought prompt call asking the model to reason step-by-step
    and provide a concise explanation alongside the final answer.
    """
    system_instruction = (
        "You are a logical reasoning assistant. Reason carefully step-by-step through the problem before answering. "
        "Provide a concise, clear explanation of your calculation/deduction followed by the final answer. "
        "Do not reveal private chain-of-thought or internal reasoning tokens."
    )
    
    prompt = question
    if context:
        prompt = f"Product Information (Mock Database):\n{context}\n\nQuestion:\n{question}"

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.0,
        max_tokens=600
    )
    
    # Return message content only (concise explanation & final answer), filtering out hidden reasoning attribute
    return response.choices[0].message.content.strip()

def main():
    print("==================================================")
    print("CHAIN-OF-THOUGHT PROMPTING DEMONSTRATION")
    print("==================================================")
    
    # Context formatted from PRODUCTS database
    products_context = json.dumps(PRODUCTS, indent=2)
    
    # Question 2: Multi-step Reasoning
    q2 = (
        "I have a budget of ₹30,000. I want a phone with at least 8 GB RAM and 256 GB storage. "
        "I also want to keep ₹3,000 as emergency money. Which phones in the available product information satisfy these requirements?"
    )
    print("\n--------------------------------------------------")
    print("QUESTION 2 — MULTI-STEP REASONING (WITH PRODUCT CONTEXT)")
    print("--------------------------------------------------")
    print(f"Question:\n{q2}\n")
    ans2 = run_chain_of_thought(q2, context=products_context)
    print(f"Answer with Step-by-Step Explanation:\n{ans2}\n")

    # Question 3: Attempting CoT without external product data
    q3 = "Which smartphone has the highest RAM among the available phones?"
    print("\n--------------------------------------------------")
    print("QUESTION 3 — EXTERNAL DATA LIMITATION DEMONSTRATION")
    print("--------------------------------------------------")
    print(f"Question:\n{q3}\n")
    ans3 = run_chain_of_thought(q3, context=None)
    print(f"Answer without Context:\n{ans3}\n")
    print("Limitation:\nChain-of-Thought improves reasoning quality over provided context, but cannot independently retrieve external information if the database is missing.")

if __name__ == "__main__":
    main()
