from __future__ import annotations

from typing import List, Dict

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
        def handle_single(ticker: str, df):
            if df is None or df.empty:
                return
            last = df.iloc[-1]
            first = df.iloc[0]
            pct_change = (last["Adj Close"] / first["Adj Close"] - 1.0) * 100.0
            results.append(
                {
                    "ticker": ticker,
                    "price": f"{last['Adj Close']:.2f}",
                    "change_5d_pct": f"{pct_change:.1f}",
                }
            )

        if isinstance(data.columns, tuple) or isinstance(data.columns, list) and isinstance(
            data.columns[0], tuple
        ):
            # Multi-index columns (multiple tickers)
            for ticker in clean:
                if ticker in data.columns.get_level_values(0):
                    df_t = data[ticker]
                    handle_single(ticker, df_t)
        else:
            # Single ticker
            handle_single(clean[0], data)

        return results

