from __future__ import annotations

from typing import List, Dict

import pandas as pd
import yfinance as yf


class MarketAgent:
    """
    Fetches basic price and trend information for a list of tickers.
    """

    def get_snapshot(self, tickers: List[str]) -> List[Dict[str, str]]:
        clean = [t.strip().upper() for t in tickers if t.strip()]
        if not clean:
            return []

        data = yf.download(
            tickers=" ".join(clean),
            period="5d",
            interval="1d",
            group_by="ticker",
            progress=False,
        )

        results: List[Dict[str, str]] = []

        # yfinance returns different shapes for single vs multiple tickers; handle both.
        def handle_single(ticker: str, df: pd.DataFrame):
            if df is None or df.empty:
                return
            # Prefer Adj Close, fall back to Close
            price_col = None
            if "Adj Close" in df.columns:
                price_col = "Adj Close"
            elif "Close" in df.columns:
                price_col = "Close"
            if price_col is None:
                return

            last = df.iloc[-1]
            first = df.iloc[0]
            pct_change = (last[price_col] / first[price_col] - 1.0) * 100.0
            results.append(
                {
                    "ticker": ticker,
                    "price": f"{last[price_col]:.2f}",
                    "change_5d_pct": f"{pct_change:.1f}",
                }
            )

        if isinstance(data.columns, pd.MultiIndex):
            # Multi-index columns (multiple tickers)
            for ticker in clean:
                if ticker in data.columns.get_level_values(0):
                    df_t = data[ticker]
                    handle_single(ticker, df_t)
        else:
            # Single ticker
            handle_single(clean[0], data)

        return results

