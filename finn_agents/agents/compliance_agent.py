from __future__ import annotations


class ComplianceAgent:
    """
    Adds disclaimers and lightly sanitizes responses to keep them educational.
    """

    DISCLAIMER = (
        "This information is for educational purposes only and is not financial, "
        "investment, tax, or legal advice. Always do your own research and consider "
        "speaking with a licensed professional before making decisions."
    )

    def wrap(self, text: str) -> str:
        cleaned = text.strip()
        # Simple heuristic to avoid imperative recommendations.
        for phrase in ["you should buy", "you must buy", "i recommend you buy"]:
            cleaned = cleaned.replace(phrase, "you may want to research")
        return f"{cleaned}\n\n---\n{self.DISCLAIMER}"

