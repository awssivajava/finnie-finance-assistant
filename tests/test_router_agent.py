from finn_agents.agents.router_agent import RouterAgent, Intent


def test_router_tab_bias_chat():
    router = RouterAgent()
    decision = router.route("hello", active_tab="Chat")
    assert decision.intent == Intent.EDUCATION


def test_router_portfolio_keywords():
    router = RouterAgent()
    decision = router.route("How should I rebalance my portfolio?", active_tab="Chat")
    assert decision.intent == Intent.PORTFOLIO


def test_router_market_keywords():
    router = RouterAgent()
    decision = router.route("What is the price of AAPL today?", active_tab="Chat")
    assert decision.intent == Intent.MARKET


def test_router_definition_etf():
    router = RouterAgent()
    decision = router.route("Explain what is an ETF", active_tab="Chat")
    assert decision.intent == Intent.EDUCATION

