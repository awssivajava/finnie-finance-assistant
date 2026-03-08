from finn_agents.models.portfolio import normalize_holdings, analyze_portfolio


def test_normalize_holdings_basic():
    raw = {"AAPL": 5000, "MSFT": 5000}
    holdings = normalize_holdings(raw)
    assert len(holdings) == 2
    assert abs(holdings[0].weight + holdings[1].weight - 1.0) < 1e-6


def test_analyze_portfolio_empty():
    analysis = analyze_portfolio({})
    assert analysis.holdings == []
    assert analysis.diversification_score == 0.0


def test_analyze_portfolio_comment_present(monkeypatch):
    # Avoid hitting yfinance in unit test by monkeypatching download
    import yfinance as yf

    def fake_download(*args, **kwargs):
        import pandas as pd
        import numpy as np

        idx = pd.date_range("2024-01-01", periods=35, freq="B")
        prices = pd.Series(100 + np.random.randn(len(idx)).cumsum(), index=idx, name="Adj Close")
        return prices.to_frame()

    monkeypatch.setattr(yf, "download", fake_download)

    analysis = analyze_portfolio({"AAPL": 7000, "MSFT": 3000})
    assert analysis.holdings
    assert 0.0 <= analysis.diversification_score <= 1.0
    assert analysis.comment != ""

