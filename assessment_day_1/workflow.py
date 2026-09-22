"""
System 2 — Rule-Based Workflow
Uses deterministic Python if/else rules and direct memory access to COURSE_FEES.
Does NOT use an LLM. Demonstrates predictability for exact rules and extreme rigidity on variations.
"""
import sys
import io
import re
from tools import COURSE_FEES
from config import QUESTIONS

# Ensure UTF-8 encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def process_query_rule_based(query: str) -> str:
    """
    Applies exact Python string pattern matching and rule execution.
    Accesses private COURSE_FEES directly without any LLM reasoning.
    """
    text = query.strip()
    
    # Rule 1: Single course fee lookup
    # Pattern: "What is the fee for AI202?"
    match_fee = re.search(r"fee for ([A-Z]{2,4}\d{3})", text, re.IGNORECASE)
    if match_fee and "scholarship" not in text.lower() and "expensive" not in text.lower():
        course_code = match_fee.group(1).upper()
        if course_code in COURSE_FEES:
            fee = COURSE_FEES[course_code]
            return f"Rs. {fee:,}"
        return f"Course '{course_code}' not found in database."

    # Rule 2: Total fee for two courses with a percentage scholarship
    # Pattern: "What is the total fee for CS101 and AI202 after a 10% scholarship?"
    match_schol = re.search(
        r"total fee for ([A-Z]{2,4}\d{3})\s+and\s+([A-Z]{2,4}\d{3})\s+after\s+a\s+(\d+)%\s+scholarship",
        text,
        re.IGNORECASE
    )
    if match_schol:
        c1, c2, pct_str = match_schol.group(1).upper(), match_schol.group(2).upper(), match_schol.group(3)
        if c1 in COURSE_FEES and c2 in COURSE_FEES:
            fee1 = COURSE_FEES[c1]
            fee2 = COURSE_FEES[c2]
            discount_pct = float(pct_str) / 100.0
            total_after_discount = (fee1 + fee2) * (1.0 - discount_pct)
            return f"Rs. {int(total_after_discount):,}"

    # Rule 3: Price comparison between two courses
    # Pattern: "Is DS303 more expensive than CS101, and by how much?"
    match_comp = re.search(
        r"Is ([A-Z]{2,4}\d{3})\s+more expensive than\s+([A-Z]{2,4}\d{3})",
        text,
        re.IGNORECASE
    )
    if match_comp:
        c1, c2 = match_comp.group(1).upper(), match_comp.group(2).upper()
        if c1 in COURSE_FEES and c2 in COURSE_FEES:
            fee1 = COURSE_FEES[c1]
            fee2 = COURSE_FEES[c2]
            diff = fee1 - fee2
            if diff > 0:
                return f"Yes, by Rs. {diff:,}"
            elif diff < 0:
                return f"No, it is cheaper by Rs. {abs(diff):,}"
            else:
                return "No, both courses have the exact same fee."

    # Rule 4: Fixed welcome message rule
    if "welcome message" in text.lower() and "ai students" in text.lower():
        return "Welcome to the AI Program at our college!\nWe are excited to have you join our innovative community."

    # Fallback when no rule matches (rigidity limitation)
    return "[Workflow Error]: Unrecognized query format. Rule-based workflow has no rule matching this input."


def run_workflow():
    print("==================================================")
    print("SYSTEM 2: RULE-BASED WORKFLOW")
    print("==================================================")
    print("Context: Pure Python logic. Direct access to COURSE_FEES dictionary. No LLM.\n")

    for i, question in enumerate(QUESTIONS, 1):
        print(f"--- Question {i} ---")
        print(f"Q: {question}")
        answer = process_query_rule_based(question)
        print(f"A: {answer}\n")


if __name__ == "__main__":
    run_workflow()
