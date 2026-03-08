from __future__ import annotations

from typing import Dict

import streamlit as st

from finn_agents import (
    RouterAgent,
    EducationAgent,
    PortfolioAgent,
    MarketAgent,
    ComplianceAgent,
    KnowledgeBase,
)


def init_session_state() -> None:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "kb" not in st.session_state:
        # Lazy-init shared knowledge base
        st.session_state.kb = KnowledgeBase()


def render_chat_tab() -> None:
    st.subheader("Chat with Finnie")
    st.write("Ask Finnie about investing concepts, markets, or how to think about portfolios.")

    history = st.session_state.chat_history
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your question about money, markets, or investing...")
    if not user_input:
        return

    history.append({"role": "user", "content": user_input})
    kb = st.session_state.kb

    router = RouterAgent()
    education = EducationAgent(kb=kb)
    portfolio = PortfolioAgent()
    market = MarketAgent()
    compliance = ComplianceAgent()

    decision = router.route(user_input, active_tab="Chat")

    reply_parts = []
    reply_parts.append(f"_Routing to intent: **{decision.intent}** ({decision.reason})_")

    try:
        if decision.intent == "education":
            reply_parts.append(education.answer(user_input))
        elif decision.intent == "portfolio":
            reply_parts.append(
                "For deeper portfolio analysis, use the **Portfolio Insights** tab. "
                "At a high level, a diversified mix of assets often reduces risk compared to a single stock."
            )
        elif decision.intent == "market":
            reply_parts.append(
                "For quick market snapshots, visit the **Market Trends** tab where you can explore specific tickers."
            )
        else:  # mixed
            reply_parts.append(education.answer(user_input))
    except Exception as exc:  # noqa: BLE001
        reply_parts.append(f"Something went wrong while processing your question: `{exc}`")

    raw_reply = "\n\n".join(reply_parts)
    final_reply = compliance.wrap(raw_reply)

    history.append({"role": "assistant", "content": final_reply})
    with st.chat_message("assistant"):
        st.markdown(final_reply)


def render_portfolio_tab() -> None:
    st.subheader("Portfolio Insights")
    st.write("Enter a few holdings to get an educational view of diversification and volatility.")

    col1, col2 = st.columns(2)
    with col1:
        tickers_str = st.text_area(
            "Tickers (comma-separated)",
            value="AAPL, MSFT, SPY",
            help="Example: AAPL, MSFT, SPY",
        )
    with col2:
        amounts_str = st.text_area(
            "Amounts (comma-separated, same order)",
            value="5000, 3000, 2000",
            help="Rough values or amounts; used only to compute weights.",
        )

    def parse_portfolio() -> Dict[str, float]:
        tickers = [t.strip() for t in tickers_str.split(",") if t.strip()]
        amounts = [a.strip() for a in amounts_str.split(",") if a.strip()]
        data: Dict[str, float] = {}
        for t, a in zip(tickers, amounts):
            try:
                data[t] = float(a)
            except ValueError:
                continue
        return data

    if st.button("Analyze portfolio"):
        holdings = parse_portfolio()
        agent = PortfolioAgent()
        compliance = ComplianceAgent()
        with st.spinner("Analyzing…"):
            try:
                text = agent.analyze(holdings)
            except Exception as exc:  # noqa: BLE001
                text = f"Something went wrong during analysis: `{exc}`"
            st.markdown(compliance.wrap(text))


def render_market_tab() -> None:
    st.subheader("Market Trends")
    st.write("Explore simple snapshots for a few popular tickers.")

    default_tickers = "SPY, QQQ, AAPL, MSFT, TSLA"
    tickers_str = st.text_input(
        "Tickers (comma-separated)",
        value=default_tickers,
        help="Example: SPY, QQQ, AAPL, MSFT, TSLA",
    )
    tickers = [t.strip() for t in tickers_str.split(",") if t.strip()]

    agent = MarketAgent()

    if st.button("Get market snapshot"):
        with st.spinner("Fetching data…"):
            try:
                rows = agent.get_snapshot(tickers)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Failed to fetch data: {exc}")
                return

        if not rows:
            st.info("No data returned for those tickers.")
            return

        st.table(rows)


def main() -> None:
    st.set_page_config(page_title="Finnie – AI Finance Assistant", layout="wide")
    st.title("Finnie – AI Finance Assistant")
    st.caption(
        "A multi-agent assistant for financial education, portfolio insights, and market awareness. "
        "For educational purposes only."
    )

    init_session_state()

    tab_chat, tab_portfolio, tab_market = st.tabs(
        ["Chat", "Portfolio Insights", "Market Trends"]
    )

    with tab_chat:
        render_chat_tab()
    with tab_portfolio:
        render_portfolio_tab()
    with tab_market:
        render_market_tab()


if __name__ == "__main__":
    main()

