import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college fee assistant. "
    "Never guess a fee. Always use get_course_fee. "
    "Use calculator for any arithmetic. "
    "Available course codes: CS101, AI202, DS303. "
    "If no tool is needed, answer directly."
)


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        # 1. REASON
        # Ask the LLM what it should do next
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            parallel_tool_calls=False,
            temperature=0
        )

        message = response.choices[0].message

        # 2. If the LLM does not request a tool,
        #    it has finished and gives the final answer
        if not message.tool_calls:
            return message.content.strip()

        # Save the LLM's tool request
        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    for call in message.tool_calls
                ]
            }
        )

        # 3. ACT + OBSERVE
        # Python executes the requested tools
        for call in message.tool_calls:

            name = call.function.name

            # Check whether the requested tool exists
            if name not in TOOL_FUNCTIONS:
                result = f"Unknown tool: {name}"

            else:
                # Convert JSON arguments into a Python dictionary
                arguments = json.loads(
                    call.function.arguments or "{}"
                )

                # Get the actual Python function
                function = TOOL_FUNCTIONS[name]

                # Execute the function
                result = function(**arguments)

                if verbose:
                    print(
                        f"   step {step}: "
                        f"{name}({arguments}) -> {result}"
                    )

            # Send the tool result back to the LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                }
            )

    # Safety limit
    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:

        print("Q:", question)

        print("A:", agent(question))

        print("-" * 70)