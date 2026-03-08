from __future__ import annotations

from typing import List, Dict

from openai import OpenAI

from .config import load_config


def _get_client() -> tuple[OpenAI, str]:
    cfg = load_config()
    client = OpenAI(api_key=cfg.openai_api_key)
    return client, cfg.openai_model


def chat_completion(
    messages: List[Dict[str, str]],
    temperature: float = 0.2,
) -> str:
    """
    Thin wrapper over OpenAI chat.completions to keep call sites simple.
    """
    client, model = _get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    content = response.choices[0].message.content
    return content or ""

