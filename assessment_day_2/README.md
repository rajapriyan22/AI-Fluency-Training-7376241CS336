# Assessment Day 2: Reasoning and Acting with Groq API

## Task Title
**"Reasoning and Acting: Comparing Direct Prompting, Chain-of-Thought, and ReAct"**

## Project Overview
This repository contains the complete implementation for **Assessment Day 2**. It demonstrates and compares four primary LLM prompting and agentic paradigms using Python and the Groq API (OpenAI-compatible client):

1. **Direct Prompting** (`direct_prompt.py`)
2. **Chain-of-Thought Prompting** (`chain_of_thought.py`)
3. **Self-Consistency Experiment** (`self_consistency.py`)
4. **ReAct Agent** (`react_agent.py`)

---

## Scenario: Smartphone Shopping Assistant

A student wants to purchase a smartphone based on budget constraints, RAM, storage, and emergency reserve funds.

> [!IMPORTANT]
> **DISCLAIMER**: The product database used in this project is **fictional mock data** created strictly for testing and demonstration purposes. It does NOT represent live market prices or real shopping websites.

### Mock Database Catalog
- **Nova X1**: ₹18,000 | 8 GB RAM | 128 GB Storage | 5000 mAh | Rating 4.2
- **PixelMax P2**: ₹24,000 | 8 GB RAM | 256 GB Storage | 5000 mAh | Rating 4.5
- **Turbo Z3**: ₹28,000 | 12 GB RAM | 256 GB Storage | 6000 mAh | Rating 4.4
- **Lite M1**: ₹15,000 | 6 GB RAM | 128 GB Storage | 5000 mAh | Rating 4.0

---

## Project Structure

```
assessment_day_2/
├── .env                  # API Key & Model Configuration (Ignored by Git)
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Project dependencies (openai, python-dotenv)
├── README.md             # Project documentation & execution guide
├── config.py             # Environment loader, Groq client, and product catalog
├── check_setup.py        # Environment & API verification script
├── direct_prompt.py      # Direct Prompting implementation
├── chain_of_thought.py   # Chain-of-Thought implementation
├── self_consistency.py   # Temperature 0.7 vs 0.0 self-consistency experiment
├── tools.py              # Mock product search tool & OpenAI tool schema
├── react_agent.py        # ReAct agent loop (Reason + Act with tool calling)
├── run_all.py            # Master runner for all paradigms
├── analysis.md           # Standalone comprehensive analysis report
└── screenshots/          # Execution screenshot guides & terminal logs
    ├── direct_prompt.png
    ├── chain_of_thought.png
    └── react_agent.png
```

---

## Setup & Installation

### 1. Prerequisites
- Python 3.10+
- Groq API Key (`GROQ_API_KEY`)

### 2. Environment Configuration
Create a `.env` file in the project root directory (`assessment_day_2/.env`):

```env
GROQ_API_KEY=your_actual_groq_api_key_here
MODEL=openai/gpt-oss-20b
```

> [!CAUTION]
> Never hard-code your API key in code files or commit `.env` to Git. `.env` is listed in `.gitignore`.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run the Scripts

### 1. Verify Setup
Verifies Python, dependencies, `.env` configuration, and Groq API connectivity:
```bash
python check_setup.py
```

### 2. Direct Prompting
Demonstrates direct single-turn responses without tools or step-by-step loops:
```bash
python direct_prompt.py
```

### 3. Chain-of-Thought Prompting
Demonstrates multi-step reasoning over provided context with concise explanations:
```bash
python chain_of_thought.py
```

### 4. Self-Consistency Experiment
Runs 5 iterations at `temperature = 0.7` vs `temperature = 0.0` to evaluate majority voting:
```bash
python self_consistency.py
```

### 5. ReAct Agent
Runs the ReAct loop (`Thought` -> `Action` -> `Observation` -> `Final Answer`) using the `search_products` tool:
```bash
python react_agent.py
```

### 6. Master Runner (Run All)
Executes all four modules sequentially in a single run:
```bash
python run_all.py
```

---

## Paradigm Summary

- **Direct Prompting**: Quick responses for simple queries. Fails when external facts are missing.
- **Chain-of-Thought**: Solves complex multi-step reasoning when full context is supplied in the prompt.
- **Self-Consistency**: Improves reasoning reliability by sampling multiple responses and taking a majority vote.
- **ReAct Agent**: Dynamically decides when to query external tools (`search_products`) to retrieve data before synthesizing the final answer.
