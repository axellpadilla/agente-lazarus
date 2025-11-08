"""Estructuras de datos utilizadas por el chatbot."""
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ChatResult:
    """Resultado estructurado al responder una pregunta."""

    question: str
    answer: str = ""
    source: str = "knowledge_base"
    transfer_to_agent: bool = False
    transfer_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "answer": self.answer,
            "source": self.source,
            "transfer_to_agent": self.transfer_to_agent,
            "transfer_reason": self.transfer_reason,
        }
