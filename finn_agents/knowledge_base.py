from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from .config import load_config


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class KnowledgeBase:
    """
    Simple RAG knowledge base built from markdown files in data/.
    """

    def __init__(self) -> None:
        cfg = load_config()
        self._embeddings = OpenAIEmbeddings(openai_api_key=cfg.openai_api_key)
        self._vectorstore = self._build_index()

    def _build_index(self) -> FAISS:
        docs: List[Document] = []
        if not DATA_DIR.exists():
            return FAISS.from_texts(["Finnie financial knowledge base is empty."], self._embeddings)

        for path in DATA_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": path.name},
                )
            )

        if not docs:
            return FAISS.from_texts(["Finnie financial knowledge base is empty."], self._embeddings)

        return FAISS.from_documents(docs, self._embeddings)

    def search(self, query: str, k: int = 4) -> List[Document]:
        return self._vectorstore.similarity_search(query, k=k)

