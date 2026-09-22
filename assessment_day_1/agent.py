"""
System 3 — AI Agent
Implements the Agent paradigm: LLM + Tools + Loop.
Uses Groq LLM to dynamically decide tool calls, executes tools safely in Python,
and loops until achieving a final answer. Prints observable step-by-step tool trace.
"""
import sys
import io
import json
from config import client, MODEL, QUESTIONS
from tools import TOOLS, TOOL_MAP

# Ensure UTF-8 output encoding for Windows console compatibility
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def run_agent_on_question(question: str) -> str:
    """
    Executes the LLM + Tools + Loop cycle for a single question.
    Only prints observable tool trace (tool name, arguments, and return values).
    """
    system_prompt = (
        "You are an AI Agent with access to tools for looking up private college course fees "
        "and performing safe calculations. "
        "DO NOT guess or invent course fees. Always use the 'get_course_fee' tool to retrieve fees for courses. "
        "Use the 'calculator' tool for any math arithmetic, discounts, or comparisons. "
        "For general creative or conversation requests (like writing a welcome message), answer directly without calling tools."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    step_counter = 1
    max_turns = 10

    for _ in range(max_turns):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.0,
            )
        except Exception as e:
            return f"[Error calling Groq API agent loop: {e}]"

        message = response.choices[0].message

        # Check if model requested tool execution
        if message.tool_calls:
            messages.append(message)  # Append assistant message with tool calls
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                raw_args = tool_call.function.arguments
                
                try:
                    args = json.loads(raw_args)
                except Exception:
                    args = {"raw": raw_args}

                # Execute tool function in Python
                if func_name in TOOL_MAP:
                    tool_func = TOOL_MAP[func_name]
                    result = tool_func(**args)
                else:
                    result = f"Error: Tool '{func_name}' is not registered."

                # Print observable tool trace step
                print(f"step {step_counter}: {func_name}({args}) -> {result}")
                step_counter += 1

                # Append tool result to message history for next turn
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": str(result),
                })
        else:
            # Final text answer produced by LLM
            return message.content.strip() if message.content else ""

    return "[Agent Warning: Exceeded maximum tool loop turns.]"


def run_agent():
    print("==================================================")
    print("SYSTEM 3: AI AGENT")
    print("==================================================")
    print(f"Provider: Groq | Model: {MODEL}")
    print("Architecture: LLM + Tools + Loop\n")

    for i, question in enumerate(QUESTIONS, 1):
        print(f"--- Question {i} ---")
        print(f"Q: {question}")
        answer = run_agent_on_question(question)
        print(f"A: {answer}\n")


if __name__ == "__main__":
    run_agent()
