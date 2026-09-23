import sys
import direct_prompt
import chain_of_thought
import self_consistency
import react_agent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    print("==================================================")
    print("ASSESSMENT DAY 2 — COMPREHENSIVE RUNNER")
    print("REASONING AND ACTING: DIRECT PROMPTING, COT, REACT")
    print("==================================================")

    # 1. Direct Prompting Demonstration
    print("\n\n" + "="*50)
    print("SECTION 1: DIRECT PROMPTING")
    print("="*50)
    direct_prompt.main()

    # 2. Chain-of-Thought Demonstration
    print("\n\n" + "="*50)
    print("SECTION 2: CHAIN-OF-THOUGHT PROMPTING")
    print("="*50)
    chain_of_thought.main()

    # 3. Self-Consistency Experiment
    print("\n\n" + "="*50)
    print("SECTION 3: SELF-CONSISTENCY EXPERIMENT")
    print("="*50)
    self_consistency.main()

    # 4. ReAct Agent Demonstration
    print("\n\n" + "="*50)
    print("SECTION 4: REACT AGENT")
    print("="*50)
    react_agent.main()

    print("\n\n==================================================")
    print("ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    main()
