import os

import pytest


@pytest.fixture(autouse=True)
def _dummy_openai_key(monkeypatch):
    """
    Ensure tests can import config-dependent modules without a real key.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    yield

