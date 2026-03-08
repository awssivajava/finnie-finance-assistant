from __future__ import annotations

from typing import Dict

from ..models.portfolio import analyze_portfolio


class PortfolioAgent:
    """
    Analyzes a simple portfolio and summarizes diversification and risk characteristics.
    """

    def analyze(self, holdings: Dict[str, float]) -> str:
        analysis = analyze_portfolio(holdings)
        if not analysis.holdings:
            return "I couldn't detect any valid holdings. Please provide tickers with positive amounts."

        lines = []
        lines.append("Here's a quick look at your portfolio (for education only, not advice):")
        holdings_str = ", ".join(
            f"{h.ticker} ({h.weight * 100:.1f}%)" for h in analysis.holdings
        )
        lines.append(f"- Holdings: {holdings_str}")
        lines.append(f"- Diversification score: {analysis.diversification_score:.2f} (0–1, higher is more diversified)")
        if analysis.volatility_30d is not None:
            lines.append(f"- Recent annualized volatility (approx.): {analysis.volatility_30d*100:.1f}%")
        lines.append("")
        lines.append(analysis.comment)
        return "\n".join(lines)

