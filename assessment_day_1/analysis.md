# Day 1 Assessment
## Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent

## 1. Scenario

The scenario modeled in this project evaluates how three distinct software architectures handle private domain data and multi-step reasoning in an educational institution setting. The college maintains proprietary tuition fee information for internal courses that is strictly private and not available in public datasets or LLM pre-training corpora.

Private data stored in Python memory (`COURSE_FEES` dictionary):
- **CS101**: Rs. 12,000
- **AI202**: Rs. 18,000
- **DS303**: Rs. 15,000

The test suite evaluates four standard operational queries and one complex constraint-based challenge question:
1. *What is the fee for AI202?* (Correct answer: Rs. 18,000)
2. *What is the total fee for CS101 and AI202 after a 10% scholarship?* (Correct answer: Rs. 27,000)
3. *Is DS303 more expensive than CS101, and by how much?* (Correct answer: Yes, by Rs. 3,000)
4. *Write a two-line welcome message for new AI students.* (General natural language generation task)
5. **Challenge Question**: *"I can pay Rs. 30,000. Which two courses can I take together within this budget?"* (Correct answer: CS101 + DS303 = Rs. 27,000, or CS101 + AI202 = Rs. 30,000).

---

## 2. Plain Chatbot

The Plain Chatbot system (`chatbot.py`) represents a direct integration with a Large Language Model (Groq API). In this architecture, user prompts are sent directly to the model without providing access to the internal private dictionary or supplying function-calling tools.

Because public LLMs are trained on general internet text, they possess no intrinsic knowledge of proprietary internal databases. When queried about private course fees, the plain chatbot cannot inspect internal systems. Depending on prompt temperature and model alignment, a plain chatbot will either explicitly state that it lacks access to private records or potentially hallucinate incorrect figures. However, for open-ended natural language generation tasks—such as composing a welcoming greeting for new students—the plain chatbot excels due to its language fluency.

The fundamental limitation observed is that a standalone LLM cannot reliably bridge the gap between general natural language generation and private organizational data without external integration mechanisms.

---

## 3. Rule-Based Workflow

The Rule-Based Workflow system (`workflow.py`) relies entirely on deterministic Python code (`if`/`else` branching, regular expressions, and string parsing). It does not incorporate any Large Language Model.

Because the workflow has direct programmatic access to the `COURSE_FEES` dictionary in Python memory, it guarantees 100% precision for exact queries that match its pre-programmed rules. It instantly retrieves the fee for AI202, accurately computes the 10% scholarship calculation for CS101 and AI202, and correctly measures the price difference between DS303 and CS101.

However, the primary limitation of a rule-based workflow is extreme rigidity. If a user rephrases a question slightly outside the expected regex pattern or presents a new combinatorial problem—such as the budget challenge question—the system fails completely, returning an unrecognized query error. Maintaining rule-based systems requires manually programming every possible question variation, which rapidly becomes unsustainable as domain complexity grows.

---

## 4. AI Agent

The AI Agent system (`agent.py`) implements the core Agent paradigm: **Agent = LLM + Tools + Loop**. It bridges the natural language understanding of an LLM with the deterministic precision of Python code execution and private data access.

The agent operates through an iterative control loop:
1. **Goal Reception**: The user prompt is received by the agent loop.
2. **LLM Decision & Tool Selection**: The Groq LLM evaluates the user prompt against registered tool schemas (`get_course_fee` and `calculator`). The LLM determines which tool to invoke and formats the required parameters.
3. **Tool Execution**: Python executes the requested tool locally (retrieving private fees from `COURSE_FEES` or calculating arithmetic via `ast` parsing).
4. **Observation**: The output of the tool execution is returned to the LLM conversation context as an observation.
5. **Iterative Reasoning Loop**: The LLM analyzes the observation and decides whether another tool call is necessary or if sufficient information exists to formulate the final answer.
6. **Final Output**: Once all required information is synthesized, the LLM outputs the final user-facing response.

For creative tasks like the welcome message, the agent recognizes that no tools are required and responds directly.

```
User Query
  │
  ▼
[ Groq LLM ] ──(Tool Request)──► [ Python Tool Execution ]
  ▲                                       │
  └───────────────(Observation)───────────┘
  │
  ▼ (Final Answer)
User Response
```

---

## 5. Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| **Flexibility** | High language flexibility; easily understands varied phrasings and creative prompts. | Extremely low; fails when input phrasing deviates from predefined regex patterns. | High; understands natural language intent and adapts tool usage dynamically. |
| **Decision-making** | Generative text generation only; cannot make operational tool decisions. | Deterministic conditional branching based strictly on pre-programmed if/else rules. | Dynamic reasoning; LLM determines which tools to call and in what sequence. |
| **Tool usage** | None; operates in isolation without function calling or external tools. | Hardcoded Python logic; directly executes internal scripts without tool abstraction. | Autonomous tool execution; calls `get_course_fee` and `calculator` as needed. |
| **Private-data access** | None; lacks access to private python memory and cannot retrieve private fees. | Direct memory access; reads `COURSE_FEES` dictionary directly within Python logic. | Controlled access; retrieves private fee data via structured `get_course_fee` tool calls. |
| **Multi-step task handling** | Poor; struggles to decompose multi-step private data queries accurately. | Rigid; handles only multi-step flows that were explicitly hardcoded in advance. | Excellent; decomposes complex queries into sequential tool calls via an iterative loop. |
| **Automation** | Limited to basic text generation and general Q&A. | Limited to routine, predictable tasks matching existing script rules. | High; autonomously plans and executes multi-step lookup and calculation workflows. |
| **Reliability** | Low for private domain facts; high risk of stating ignorance or hallucination. | High for exact matched inputs; zero reliability for unprogrammed edge cases. | High; combines factual data from tools with verified calculator outputs. |

---

## 6. Results

The empirical results observed across all three systems during execution are summarized below:

### Question 1: *"What is the fee for AI202?"*
- **Plain Chatbot**: States that it does not possess access to private internal fee schedules and suggests checking the official course catalog.
- **Rule-Based Workflow**: Successfully matches Rule 1 and returns `Rs. 18,000`.
- **AI Agent**: Calls `get_course_fee({'course_code': 'AI202'}) -> 18000` and returns `₹18,000`.

### Question 2: *"What is the total fee for CS101 and AI202 after a 10% scholarship?"*
- **Plain Chatbot**: States that it lacks fee information for CS101 and AI202 and cannot compute the total.
- **Rule-Based Workflow**: Successfully matches Rule 2, calculates `(12000 + 18000) * 0.9` directly in Python, and returns `Rs. 27,000`.
- **AI Agent**: Executes a 3-step tool loop (`get_course_fee` for CS101, `get_course_fee` for AI202, and `calculator` for `(12000 + 18000) * 0.9`), returning `₹27,000`.

### Question 3: *"Is DS303 more expensive than CS101, and by how much?"*
- **Plain Chatbot**: Explains that it lacks pricing data for DS303 and CS101 and cannot compare them.
- **Rule-Based Workflow**: Matches Rule 3, computes `15000 - 12000 = 3000`, and returns `Yes, by Rs. 3,000`.
- **AI Agent**: Executes tool calls to retrieve fees for DS303 and CS101, uses `calculator` to evaluate `15000 - 12000`, and confirms DS303 is `Rs 3,000 more expensive`.

### Question 4: *"Write a two-line welcome message for new AI students."*
- **Plain Chatbot**: Generates a creative, fluent two-line greeting.
- **Rule-Based Workflow**: Returns a hardcoded static welcome message string.
- **AI Agent**: Recognizes no tools are needed and generates a warm, fluent two-line welcome message.

### Challenge Question: *"I can pay Rs. 30,000. Which two courses can I take together within this budget?"*
- **Plain Chatbot**: Cannot perform private database lookup or accurate arithmetic optimization.
- **Rule-Based Workflow**: Returns `[Workflow Error]: Unrecognized query format` because combinatorial budget optimization was not hardcoded into its rule set.
- **AI Agent**: Dynamically queries course fees, uses the `calculator` tool to sum course combinations (`12000 + 18000 = 30000` and `12000 + 15000 = 27000`), and identifies that `CS101 + DS303` (or `CS101 + AI202`) fits within the Rs. 30,000 budget.

---

## 7. Suitability Analysis

For this specific private college course-fee scenario, the **AI Agent** approach is the most suitable architecture.

### Justification:
1. **Private-Data Access & Security**: The AI agent accesses proprietary fees strictly through defined Python tools without exposing internal data structures to model pre-training.
2. **Flexibility & Natural Language Interface**: Students ask questions in varied ways. The agent understands natural language intent, eliminating the rigid pattern failures of rule-based scripts.
3. **Multi-Step Problem Solving**: Questions requiring lookup followed by arithmetic (such as scholarship calculation or budget pairing) are naturally handled through the agent's iterative reasoning loop.
4. **Reliability**: Arithmetic is delegated to Python's `calculator` tool rather than relying on LLM mental math, eliminating calculation errors.

### Architectural Trade-offs:
- **Plain Chatbot Trade-off**: Lowest latency and simplest implementation, but completely incapable of handling private data.
- **Rule-Based Workflow Trade-off**: Zero API costs and 100% deterministic speed for known inputs, but fragile and expensive to maintain as rules multiply.
- **AI Agent Trade-off**: Superior capabilities and adaptability, balanced against higher API latency, token consumption, and the need for tool execution guardrails.

---

## 8. Conclusion

Each system architecture serves a distinct purpose depending on operational requirements:

- **Plain Chatbot**: Appropriate when users require general conversational guidance, language translation, creative writing, or information summarization from public domain knowledge, where private data access and action execution are unnecessary. *(Real-world example: A public university website FAQ bot for prospective students asking general campus directions).*
- **Rule-Based Workflow**: Ideal for strict, highly structured, invariant business logic where rules are static, inputs are predictable, and absolute deterministic precision is required without API overhead. *(Real-world example: An automated payroll tax calculation script or standard bank fee deduction engine).*
- **AI Agent**: Necessary when handling dynamic customer inquiries, multi-step problem solving, private enterprise database lookup, and automated task execution across external APIs. *(Real-world example: An enterprise academic advising assistant that checks student transcript records, evaluates degree prerequisite fulfillment, and calculates tuition balances dynamically).*

---

## 9. Agent Tool Trace

Below is an observable tool trace recorded during the execution of Question 2 (*"What is the total fee for CS101 and AI202 after a 10% scholarship?"*):

```text
Step 1:
get_course_fee({'course_code': 'CS101'})
→ 12000

Step 2:
get_course_fee({'course_code': 'AI202'})
→ 18000

Step 3:
calculator({'expression': '(12000 + 18000) * 0.9'})
→ 27000
```

### Demonstration of Agent Principles (LLM + Tools + Loop):
- **LLM**: Decides that `CS101` fee is missing, calls `get_course_fee`.
- **Tools**: Python executes `get_course_fee('CS101')` and returns `12000`.
- **Loop**: The LLM receives `12000`, realizes `AI202` fee is still needed, and issues a second tool call for `AI202`.
- **Observation & Action**: Upon receiving `18000`, the LLM recognizes that arithmetic is required and invokes `calculator` with expression `(12000 + 18000) * 0.9`.
- **Final Result**: The returned observation `27000` is synthesized into the clear final answer: *"The total fee after a 10% scholarship is Rs. 27,000."*

---

## 10. How to Run

Follow these steps to set up and run the project locally on Windows:

### 1. Create Virtual Environment
```cmd
python -m venv .venv
```

### 2. Activate Virtual Environment (Windows)
```cmd
.venv\Scripts\activate
```

### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 4. Configure Local `.env` File
Create a `.env` file in the root of `assessment_day_1/` (this file is ignored by Git and must never be committed):
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL=openai/gpt-oss-20b
```

### 5. Verify Setup & API Connection
```cmd
python check_setup.py
```

### 6. Run Individual Systems
```cmd
python chatbot.py
python workflow.py
python agent.py
python challenge.py
```

### 7. (Optional) Re-generate Output Terminal Screenshots
```cmd
python generate_outputs.py
```
