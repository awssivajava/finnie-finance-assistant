from __future__ import annotations

from typing import List

from langchain_core.documents import Document

from ..knowledge_base import KnowledgeBase
from ..llm_client import chat_completion


class EducationAgent:
    """
    Uses the RAG knowledge base to explain financial concepts in a beginner-friendly way.
    """

    def __init__(self, kb: KnowledgeBase | None = None) -> None:
        self.kb = kb or KnowledgeBase()

    def answer(self, question: str) -> str:
        docs: List[Document] = self.kb.search(question, k=4)
        context_snippets = "\n\n".join(
            f"From {d.metadata.get('source', 'kb')}:\n{d.page_content[:600]}" for d in docs
        )
        prompt = [
            {
                "role": "system",
                "content": (
                    "You are Finnie, a friendly financial education assistant. "
                    "Explain concepts clearly with simple language. "
                    "Use ONLY the provided context; if unsure, say you are not sure. "
                    "Do not give direct investment recommendations or tell the user to buy or sell specific assets."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Context from knowledge base:\n{context_snippets}\n\n"
                    f"User question: {question}\n\n"
                    "Answer in 2–5 short paragraphs, with concrete examples when helpful."
                ),
            },
        ]
        return chat_completion(prompt)

