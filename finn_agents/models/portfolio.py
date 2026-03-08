from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

import numpy as np
import pandas as pd
import yfinance as yf


@dataclass
class Holding:
    ticker: str
    weight: float  # 0–1


@dataclass
class PortfolioAnalysis:
    holdings: List[Holding]
    diversification_score: float
    volatility_30d: float | None
    comment: str


def normalize_holdings(raw: Dict[str, float]) -> List[Holding]:
    tickers = [t.strip().upper() for t in raw.keys() if t.strip()]
    values = np.array(list(raw.values()), dtype=float)
    total = float(values.sum())
    if total <= 0 or len(tickers) == 0:
        return []
    weights = values / total
    return [Holding(ticker=t, weight=float(w)) for t, w in zip(tickers, weights)]


def analyze_portfolio(raw: Dict[str, float]) -> PortfolioAnalysis:
    holdings = normalize_holdings(raw)
    if not holdings:
        return PortfolioAnalysis(
            holdings=[],
            diversification_score=0.0,
            volatility_30d=None,
            comment="No valid holdings provided.",
        )

    # Diversification: simple entropy-based score
    weights = np.array([h.weight for h in holdings])
    entropy = -np.sum(weights * np.log(weights + 1e-9))
    max_entropy = np.log(len(weights))
    diversification_score = float(entropy / max_entropy) if max_entropy > 0 else 0.0

    # Volatility: 30 trading days of daily returns for equal-weighted portfolio of given tickers
    tickers_str = " ".join(h.ticker for h in holdings)
    hist = yf.download(tickers=tickers_str, period="2mo", interval="1d", progress=False)
    vol_30d: float | None = None
    if not hist.empty:
        # Handle both single- and multi-ticker shapes from yfinance.
        prices: pd.DataFrame | None = None
        if isinstance(hist.columns, pd.MultiIndex):
            # Multi-index: (ticker, field)
            try:
                prices = hist.xs("Adj Close", axis=1, level=1)
            except KeyError:
                try:
                    prices = hist.xs("Close", axis=1, level=1)
                except KeyError:
                    prices = None
        else:
            if "Adj Close" in hist.columns:
                prices = hist[["Adj Close"]]
            elif "Close" in hist.columns:
                prices = hist[["Close"]]

        if prices is not None and not prices.empty:
            rets = prices.pct_change().dropna()
            if len(rets) >= 30:
                last_30 = rets.tail(30)
                port_rets = last_30.mean(axis=1)
                vol_30d = float(port_rets.std()) * np.sqrt(252)

    comment_parts = []
    if diversification_score < 0.4:
        comment_parts.append("Portfolio appears concentrated; consider adding more uncorrelated assets.")
    elif diversification_score < 0.7:
        comment_parts.append("Portfolio has moderate diversification.")
    else:
        comment_parts.append("Portfolio looks well diversified across holdings.")

    if vol_30d is not None:
        if vol_30d > 0.25:
            comment_parts.append("Recent volatility is relatively high; ensure this matches your risk tolerance.")
        elif vol_30d < 0.12:
            comment_parts.append("Recent volatility is relatively low; suitable for more conservative profiles.")

    comment = " ".join(comment_parts)

    return PortfolioAnalysis(
        holdings=holdings,
        diversification_score=diversification_score,
        volatility_30d=vol_30d,
        comment=comment,
    )

