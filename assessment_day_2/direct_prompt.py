import sys
from config import client, MODEL

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_direct_prompt(question: str, context: str = None) -> str:
    """
    Executes a direct prompt call to the LLM without tools or multi-step loops.
    """
    messages = []
    system_instruction = (
        "You are a helpful assistant. Answer the user's question directly and concisely. "
        "Do not output hidden reasoning or private chain-of-thought tokens."
    )
    messages.append({"role": "system", "content": system_instruction})
    
    prompt = question
    if context:
        prompt = f"Context:\n{context}\n\nQuestion:\n{question}"
        
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.0,
        max_tokens=500
    )
    
    # Return content only, strictly excluding any reasoning attribute
    return response.choices[0].message.content.strip()

def main():
    print("==================================================")
    print("DIRECT PROMPTING DEMONSTRATION")
    print("==================================================")
    
    # Question 1: Simple Reasoning (Calculations)
    q1 = "I have a budget of ₹25,000. If I buy a phone for ₹18,000 and a phone case for ₹800, how much money will remain?"
    print("\n--------------------------------------------------")
    print("QUESTION 1 — SIMPLE REASONING")
    print("--------------------------------------------------")
    print(f"Question:\n{q1}\n")
    ans1 = run_direct_prompt(q1)
    print(f"Answer:\n{ans1}\n")
    print("Limitation:\nNo external tools are available.")

    # Question 3: External Tool Question (Attempted via Direct Prompting without context)
    q3 = "Which smartphone has the highest RAM among the available phones?"
    print("\n--------------------------------------------------")
    print("QUESTION 3 — EXTERNAL INFORMATION LOOKUP")
    print("--------------------------------------------------")
    print(f"Question:\n{q3}\n")
    ans3 = run_direct_prompt(q3)
    print(f"Answer:\n{ans3}\n")
    print("Limitation:\nNo external tools are available. Direct prompting cannot query an external database unless product details are explicitly pasted into the prompt.")

if __name__ == "__main__":
    main()
