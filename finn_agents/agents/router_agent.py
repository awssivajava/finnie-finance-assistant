from __future__ import annotations

from dataclasses import dataclass


class Intent(str):
    EDUCATION = "education"
    PORTFOLIO = "portfolio"
    MARKET = "market"
    MIXED = "mixed"


@dataclass
class RoutingDecision:
    intent: str
    reason: str


class RouterAgent:
    """
    Lightweight heuristic router for Finnie.
    Determines which specialist agent(s) should handle a user query.
    """

    @staticmethod
    def route(user_message: str, active_tab: str) -> RoutingDecision:
        text = (user_message or "").lower()

        # Tab-based bias
        if active_tab == "Portfolio Insights":
            base_intent = Intent.PORTFOLIO
        elif active_tab == "Market Trends":
            base_intent = Intent.MARKET
        else:
            base_intent = Intent.EDUCATION

        # Keyword-based refinements
        if any(word in text for word in ["my portfolio", "holdings", "allocation", "rebalance"]):
            return RoutingDecision(intent=Intent.PORTFOLIO, reason="Mentions portfolio-related keywords.")

        definition_cues = [
            "what is",
            "what are",
            "explain",
            "tell me about",
            "overview of",
            "basics of",
            "difference between",
            "meaning of",
            "define",
            "definition of",
        ]
        market_data_cues = [
            "price",
            "quote",
            "today",
            "market",
            "index",
            "trend",
            "performance",
            "returns",
            "volatility",
            "chart",
            "ytd",
            "%",
            "percent",
            "change",
        ]
        instrument_terms = ["stock", "etf", "bond", "mutual fund", "fund", "ticker"]

        if any(word in text for word in definition_cues) and not any(word in text for word in market_data_cues):
            return RoutingDecision(intent=Intent.EDUCATION, reason="Conceptual explanation requested.")

        if any(word in text for word in market_data_cues) or any(word in text for word in instrument_terms):
            if base_intent == Intent.PORTFOLIO:
                return RoutingDecision(intent=Intent.MIXED, reason="Blend of market and portfolio questions.")
            return RoutingDecision(intent=Intent.MARKET, reason="Mentions market-related keywords.")

        return RoutingDecision(intent=base_intent, reason="Fallback to tab-based intent.")

