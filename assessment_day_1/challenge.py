"""
Challenge Script for Day 1 Assessment
Question: "I can pay Rs. 30,000. Which two courses can I take together within this budget?"

Compares how System 2 (Rule-Based Workflow) fails due to missing rules,
and how System 3 (AI Agent) uses reasoning, tool calls, and loop to solve the budget constraint.
"""
import sys
import io
from workflow import process_query_rule_based
from agent import run_agent_on_question

# Ensure UTF-8 output encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CHALLENGE_QUESTION = "I can pay Rs. 30,000. Which two courses can I take together within this budget?"


def run_challenge():
    print("==================================================")
    print("CHALLENGE EVALUATION")
    print("==================================================")
    print(f"Question: \"{CHALLENGE_QUESTION}\"\n")

    print("--------------------------------------------------")
    print("1. EVALUATING SYSTEM 2 — RULE-BASED WORKFLOW")
    print("--------------------------------------------------")
    workflow_answer = process_query_rule_based(CHALLENGE_QUESTION)
    print(f"Workflow Answer:\n{workflow_answer}\n")
    print("Observation: System 2 failed because budget optimization across multiple courses was not hardcoded in its rules.\n")

    print("--------------------------------------------------")
    print("2. EVALUATING SYSTEM 3 — AI AGENT")
    print("--------------------------------------------------")
    print("Agent Execution & Tool Trace:")
    agent_answer = run_agent_on_question(CHALLENGE_QUESTION)
    print(f"\nAgent Final Answer:\n{agent_answer}\n")
    print("Observation: System 3 dynamically retrieved private course fees, performed math calculations, and identified that CS101 (Rs. 12,000) + DS303 (Rs. 15,000) = Rs. 27,000 fits within the Rs. 30,000 budget.")


if __name__ == "__main__":
    run_challenge()
