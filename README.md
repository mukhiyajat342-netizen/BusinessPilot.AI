# BusinessPilot AI

**One business problem. Multiple expert agents. One actionable plan.**

BusinessPilot AI is a multi-agent business-planning prototype for small businesses. A central Orchestrator coordinates research, strategy, specialist recommendations, illustrative finance allocation, execution planning, and evaluation.

## Current capabilities

- Business profile and problem input
- Research hypotheses based on user-provided context
- Strategy generation
- Keyword-based dynamic selection of Marketing, Customer Support, Operations, and Sales specialists
- Shared in-memory state and agent-to-agent message log
- Task-level illustrative budget allocation
- Execution schedule across a requested planning period
- Evaluation and up to two improvement attempts
- Streamlit interface and terminal demo

## Important prototype limitations

This version is a deterministic, rule-based prototype. It does **not** perform verified live market research, connect to real sales systems, or use an LLM. Research findings are hypotheses. Budget allocations are illustrative equal splits, not vendor quotes or financial advice. A human should verify costs and approve any real-world action.

## Requirements

- Python 3.10+
- pip
- macOS, Windows, or Linux

## Setup (macOS / Linux)

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd BusinessPilot_AI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run terminal demo

```bash
python main.py
```

## Run frontend

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
BusinessPilot_AI/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── src/
│   └── businesspilot/
│       ├── schemas.py
│       ├── state.py
│       └── agents/
│           ├── agent_selector.py
│           ├── customer_support.py
│           ├── evaluation.py
│           ├── execution.py
│           ├── finance.py
│           ├── marketing.py
│           ├── operations.py
│           ├── orchestrator.py
│           ├── research.py
│           ├── sales.py
│           └── strategy.py
└── tests/
    └── test_workflow.py
```

## Agent workflow

```text
Business Request
      |
      v
 Orchestrator
      |
      +--> Research Agent
      |
      +--> Strategy Agent
      |
      +--> Dynamic Specialist Selection
      |       +--> Marketing
      |       +--> Customer Support
      |       +--> Operations
      |       +--> Sales
      |
      +--> Finance Agent
      |
      +--> Execution Agent
      |
      +--> Evaluation Agent
              |
              +--> Feedback / Revision (up to 2 attempts)
              |
              v
        Final Business Plan
```

## GitHub publishing

Before pushing, verify `.env` is ignored and do not commit API keys, passwords, personal data, or private business records.

```bash
git status --short
git add .
git status --short
git commit -m "Build BusinessPilot AI multi-agent prototype"
git push
```

If this is a new GitHub repository, create an empty repository on GitHub first, then connect its URL:

```bash
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git branch -M main
git push -u origin main
```

Do not publish `.env` or `.venv/`.
