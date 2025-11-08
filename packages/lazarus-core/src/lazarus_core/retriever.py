"""Modulos de recuperacion compatibles con DSPy."""

from typing import Dict, List, Optional

import dspy

from lazarus_kb import FAQKnowledgeBase


class FAQRetriever(dspy.Module):
    """Recupera pasajes de la base de conocimiento de FAQ para DSPy."""

    def __init__(self, knowledge_base: FAQKnowledgeBase, *, k: int = 1) -> None:
        super().__init__()
        self.kb = knowledge_base
        self.k = k

    def forward(self, query: str) -> dspy.Prediction:
        match = self.kb.search(query)
        passages: List[str] = []
        metadata: Optional[Dict[str, str]] = None

        if match:
            formatted = (
                f"Pregunta relacionada: {match.get('pregunta', '')}\n"
                f"Respuesta: {match.get('respuesta', '')}"
            )
            passages.append(formatted)
            metadata = match

        return dspy.Prediction(passages=passages, metadata=metadata)
