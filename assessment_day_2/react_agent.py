import sys
import json
from config import client, MODEL
from tools import search_products, SEARCH_PRODUCTS_TOOL

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_react_agent(question: str, max_iterations: int = 5) -> str:
    """
    Executes a ReAct agent loop using OpenAI function calling on Groq API.
    Prints safe high-level trace information (Thought Summary, Action, Observation, Final Answer)
    without revealing hidden chain-of-thought or raw reasoning tokens.
    """
    system_instruction = (
        "You are a smartphone shopping assistant. "
        "When asked about smartphone specifications, prices, RAM, storage, or recommendations, "
        "use the `search_products` tool to fetch accurate product data. "
        "For simple math or general logic, answer directly without tools. "
        "Never output hidden chain-of-thought or private reasoning tokens."
    )

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": question}
    ]

    tools = [SEARCH_PRODUCTS_TOOL]

    print(f"\n[Question] {question}")

    for iteration in range(1, max_iterations + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=False,
                temperature=0.0,
                max_tokens=600
            )
        except Exception as e:
            print(f"[Error] API call failed on iteration {iteration}: {e}")
            return f"Error: API execution failed - {e}"

        message = response.choices[0].message
        messages.append(message)

        # Check if model invoked a tool
        if message.tool_calls:
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args_raw = tool_call.function.arguments

                # Parse tool arguments safely
                try:
                    func_args = json.loads(func_args_raw)
                except json.JSONDecodeError:
                    func_args = {"query": func_args_raw}

                query = func_args.get("query", "")

                print(f"\n[Thought Summary] External product information is required to answer accurately.")
                print(f"[Action] {func_name}({{\"query\": \"{query}\"}})")

                # Execute tool
                if func_name == "search_products":
                    observation = search_products(query)
                else:
                    observation = json.dumps({"error": f"Unknown tool: {func_name}"})

                # Display concise observation summary
                try:
                    obs_dict = json.loads(observation)
                    res = obs_dict.get("results", {})
                    match_type = obs_dict.get("match_type", "")
                    if isinstance(res, dict):
                        summary_str = ", ".join([f"{k} ({v.get('ram', '')}GB RAM, ₹{v.get('price', '')})" for k, v in res.items()])
                    else:
                        summary_str = str(res)
                    print(f"[Observation] Search match '{match_type}': {summary_str}")
                except Exception:
                    print(f"[Observation] {observation[:150]}...")

                # Append tool observation to conversation history
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": observation
                })

        elif message.content:
            # Final answer reached
            final_answer = message.content.strip()
            print(f"\n[Final Answer]\n{final_answer}")
            return final_answer
        else:
            print(f"[Warning] Iteration {iteration}: Model returned empty content and no tool calls.")
            break

    return "ReAct agent reached maximum iterations without a final answer."

def main():
    print("==================================================")
    print("REACT AGENT DEMONSTRATION")
    print("==================================================")

    # Test Question 1: Simple Reasoning (Calculations)
    print("\n--------------------------------------------------")
    print("REACT TEST 1 — SIMPLE REASONING (CALCULATION)")
    print("--------------------------------------------------")
    q1 = "I have a budget of ₹25,000. If I buy a phone for ₹18,000 and a phone case for ₹800, how much money will remain?"
    run_react_agent(q1)

    # Test Question 2: Multi-step Reasoning
    print("\n--------------------------------------------------")
    print("REACT TEST 2 — MULTI-STEP REASONING (SELECTION)")
    print("--------------------------------------------------")
    q2 = "I have a budget of ₹30,000. I want a phone with at least 8 GB RAM and 256 GB storage. I also want to keep ₹3,000 as emergency money. Which phones satisfy these requirements?"
    run_react_agent(q2)

    # Test Question 3: Tool-required External Information Lookup
    print("\n--------------------------------------------------")
    print("REACT TEST 3 — EXTERNAL INFORMATION LOOKUP (TOOL TRIGGER)")
    print("--------------------------------------------------")
    q3 = "Which smartphone has the highest RAM?"
    run_react_agent(q3)

if __name__ == "__main__":
    main()
