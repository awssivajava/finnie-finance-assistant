from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st


@dataclass
class AppConfig:
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"


def load_config() -> AppConfig:
    """
    Load configuration, preferring Streamlit secrets when available.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Prefer Streamlit secrets if present
    try:
        if "openai" in st.secrets:
            api_key = st.secrets["openai"].get("api_key", api_key)
            model = st.secrets["openai"].get("model", model)
    except Exception:
        # st.secrets may not be available in non-Streamlit contexts
        pass

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. "
            "Set it in environment variables or .streamlit/secrets.toml."
        )

    return AppConfig(openai_api_key=api_key, openai_model=model)

