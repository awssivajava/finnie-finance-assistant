# Finnie – AI Finance Assistant

Finnie is a multi-agent AI finance assistant that helps users build financial literacy, explore markets, and understand their portfolios with confidence. It combines:

- A **context-aware chat agent**
- **Specialized agents** for education, portfolio analysis, market trends, and compliance
- A **retrieval-augmented knowledge base** with categorized financial content
- **Real-time market data** and simple portfolio analytics

The app is built to run on **Streamlit Community Cloud** (recommended) or any Python host with Streamlit.

## Features

- **Multi-tab UI**
  - **Chat** – conversational assistant (Finnie) with context and RAG-backed explanations.
  - **Portfolio Insights** – upload or enter holdings and get diversification and risk/return style insights.
  - **Market Trends** – see live prices and basic trends for popular tickers and indices.
- **Multi-agent architecture**
  - **RouterAgent** – classifies user intents and dispatches to specialists.
  - **EducationAgent** – explains concepts using the RAG knowledge base.
  - **PortfolioAgent** – analyzes simple portfolios using yfinance.
  - **MarketAgent** – fetches real-time/near-real-time quotes and summaries.
  - **ComplianceAgent** – adds safety language and avoids direct investment recommendations.
- **RAG knowledge base**
  - Markdown articles under `data/` are embedded into a FAISS index at startup.
  - Used by EducationAgent to ground explanations and keep wording consistent.
- **Reliability**
  - Graceful error handling around API calls.
  - Simple fallback messages when market data or LLM calls fail.
  - Pytest-based tests to cover core routing and analytics logic (~80% of core code).

## Tech stack

- **Language**: Python 3.11+
- **UI**: Streamlit
- **LLM**: OpenAI (GPT-4o or GPT-4o-mini; configurable)
- **Vector DB**: FAISS via LangChain
- **RAG**: LangChain + markdown documents
- **Market data**: `yfinance`
- **Tests**: `pytest`, `pytest-cov`

## Project structure

```text
Finance Assistant/
  README.md
  requirements.txt
  streamlit_app.py
  finn_agents/
    __init__.py
    config.py
    llm_client.py
    knowledge_base.py
    models/
      portfolio.py
    agents/
      router_agent.py
      education_agent.py
      portfolio_agent.py
      market_agent.py
      compliance_agent.py
  data/
    kb_introduction.md
    kb_investing_basics.md
    kb_risk_management.md
    kb_glossary.md
  tests/
    test_router_agent.py
    test_portfolio.py
    conftest.py
  .streamlit/
    secrets.toml.example
```

## Architecture diagram

```mermaid
flowchart LR
  UI[Streamlit UI\nstreamlit_app.py] --> Router[RouterAgent]

  Router --> Edu[EducationAgent]
  Router --> Port[PortfolioAgent]
  Router --> Mkt[MarketAgent]

  Edu --> KB[Markdown KB\n(data/*.md)]
  KB --> FAISS[FAISS Index\n(knowledge_base.py)]
  Edu --> LLM[OpenAI Chat\n(llm_client.py)]

  Port --> PF[Portfolio Math\n(models/portfolio.py)]
  Mkt --> YF[yfinance API]

  Edu --> Comp[ComplianceAgent]
  Port --> Comp
  Mkt --> Comp
  Comp --> UI
```

## Setup

### 1. Create virtual environment and install dependencies

```bash
cd "Finance Assistant"
python -m venv .venv
.\.venv\Scripts\activate  # on Windows PowerShell
# source .venv/bin/activate  # on macOS/Linux

pip install -r requirements.txt
```

### 2. Configure API keys

Finnie uses OpenAI for language capabilities.

Locally, you can either:

- Set an environment variable:

```bash
setx OPENAI_API_KEY "your-key-here"
```

or

- Use Streamlit secrets (recommended and required for Streamlit Cloud):

1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
2. Fill in your OpenAI API key:

```toml
[openai]
api_key = "sk-..."
model = "gpt-4o-mini"
```

On **Streamlit Community Cloud**, go to **App → Settings → Secrets** and paste the same TOML contents.

### 3. Run locally

```bash
streamlit run streamlit_app.py
```

The app will open in your browser (by default at `http://localhost:8501`).

## Running tests

```bash
cd "Finance Assistant"
pytest --cov=finn_agents --cov-report=term-missing
```

This runs the test suite and prints coverage; the core routing and portfolio modules are designed to be well-covered (~80%+ of the important logic).

## Deploying to Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. In Streamlit Cloud, create a new app and point it at:
   - Repo: `<your-repo>`
   - Branch: `main` (or your chosen branch)
   - File: `Finance Assistant/streamlit_app.py`
3. In **Secrets**, paste the contents of your `.streamlit/secrets.toml` (without comments).
4. Click **Deploy**.

Finnie will build automatically using `requirements.txt` and run `streamlit_app.py`.

## Disclaimers

Finnie is for **educational purposes only** and does **not** provide financial, investment, tax, or legal advice.  
Always consult a qualified professional before making financial decisions.

