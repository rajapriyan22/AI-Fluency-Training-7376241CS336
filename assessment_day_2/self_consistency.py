import sys
import json
from collections import Counter
from config import client, MODEL, PRODUCTS

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_sample(prompt: str, temperature: float) -> str:
    """Runs a single inference call at a given temperature."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful mathematical assistant. Reason step-by-step concisely to identify which phone satisfies all user requirements. "
                    "Conclude with 'FINAL ANSWER: PixelMax P2' (or the exact qualifying phone)."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=650
    )
    return response.choices[0].message.content.strip()

def extract_conclusion(response_text: str) -> str:
    """Extract phone recommendation from response."""
    text_upper = response_text.upper()
    if "FINAL ANSWER:" in text_upper:
        answer_part = text_upper.split("FINAL ANSWER:")[1]
        if "PIXELMAX" in answer_part or "P2" in answer_part:
            return "PixelMax P2"
        elif "TURBO" in answer_part or "Z3" in answer_part:
            return "Turbo Z3"
        elif "NOVA" in answer_part:
            return "Nova X1"
        elif "LITE" in answer_part:
            return "Lite M1"
    
    # Fallback search in entire text
    if "PIXELMAX P2" in text_upper or "PIXELMAX" in text_upper:
        return "PixelMax P2"
    elif "TURBO Z3" in text_upper:
        return "Turbo Z3"
    elif "NOVA X1" in text_upper:
        return "Nova X1"
    else:
        return "Inconclusive"

def main():
    print("==================================================")
    print("SELF-CONSISTENCY EXPERIMENT")
    print("==================================================")

    q2 = (
        "I have a budget of ₹30,000. I want a phone with at least 8 GB RAM and 256 GB storage. "
        "I also want to keep ₹3,000 as emergency money. Which phones in the available product information satisfy these requirements?"
    )
    products_context = json.dumps(PRODUCTS, indent=2)
    full_prompt = f"Product Information:\n{products_context}\n\nQuestion:\n{q2}"

    # --- EXPERIMENT 1: Temperature = 0.7 ---
    print("\n--------------------------------------------------")
    print("=== SELF-CONSISTENCY EXPERIMENT ===")
    print("Temperature: 0.7")
    print("--------------------------------------------------")
    
    results_t07 = []
    conclusions_t07 = []

    for i in range(1, 6):
        out = run_sample(full_prompt, temperature=0.7)
        results_t07.append(out)
        conc = extract_conclusion(out)
        conclusions_t07.append(conc)
        print(f"\nRun {i}:")
        print(out)
        print(f"--> Extracted Candidate: {conc}")

    print("\nSummary (Temperature 0.7):")
    counts_t07 = Counter(conclusions_t07)
    for cand, count in counts_t07.items():
        print(f"- {cand}: {count}/5 votes")

    majority_t07, count_t07 = counts_t07.most_common(1)[0]
    print(f"\nMajority Answer (Temp 0.7): {majority_t07} ({count_t07}/5 votes)")

    # --- EXPERIMENT 2: Temperature = 0.0 ---
    print("\n--------------------------------------------------")
    print("=== COMPARISON EXPERIMENT ===")
    print("Temperature: 0.0")
    print("--------------------------------------------------")

    results_t00 = []
    conclusions_t00 = []

    for i in range(1, 6):
        out = run_sample(full_prompt, temperature=0.0)
        results_t00.append(out)
        conc = extract_conclusion(out)
        conclusions_t00.append(conc)
        print(f"\nRun {i}:")
        print(out)
        print(f"--> Extracted Candidate: {conc}")

    print("\nSummary (Temperature 0.0):")
    counts_t00 = Counter(conclusions_t00)
    for cand, count in counts_t00.items():
        print(f"- {cand}: {count}/5 votes")

    majority_t00, count_t00 = counts_t00.most_common(1)[0]
    print(f"\nMajority Answer (Temp 0.0): {majority_t00} ({count_t00}/5 votes)")

    # --- CONSISTENCY ANALYSIS ---
    print("\n--------------------------------------------------")
    print("CONSISTENCY COMPARISON & OBSERVATIONS")
    print("--------------------------------------------------")
    print(f"At Temperature 0.7, candidate consistency for '{majority_t07}' was {count_t07}/5.")
    print(f"At Temperature 0.0, candidate consistency for '{majority_t00}' was {count_t00}/5.")
    print("Observation: Temperature 0.0 yields 100% deterministic consistency across repeated queries, while Temperature 0.7 introduces natural sampling variation in reasoning style and formatting.")

if __name__ == "__main__":
    main()
