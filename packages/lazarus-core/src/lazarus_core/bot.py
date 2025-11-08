"""Modulo principal del chatbot Lazarus."""

import os
from typing import Dict, Optional, Sequence, Tuple

import dspy

from lazarus_kb import FAQKnowledgeBase

from .constants import (
    AGENT_CONTEXT_LIMIT,
    SMALL_TALK_PHRASES,
    SMALL_TALK_PREFIXES,
    TRANSFER_MESSAGES,
)
from .retriever import FAQRetriever
from .signatures import CustomerServiceSignature, TransferDecisionSignature
from .structures import ChatResult


class LazarusChatbot(dspy.Module):
    """Chatbot inteligente para Grupo Lazarus."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        excel_file: Optional[str] = None,
    ) -> None:
        super().__init__()

        self.api_key = api_key or os.getenv("DSPY_API_KEY")
        self.model = model or os.getenv("DSPY_MODEL")
        self.api_base = os.getenv("DSPY_API_BASE")

        if not self.api_key or not self.model:
            print(
                "Advertencia: No se proporcionaron clave API o modelo. Establezca las variables de entorno DSPY_API_KEY y DSPY_MODEL."
            )
            print("Ejecutandose en modo demo con funcionalidad limitada.")

        if excel_file is None:
            excel_file = "./data_limpia/faq_limpio.csv"

        self.kb = FAQKnowledgeBase(excel_file)
        self.retriever = FAQRetriever(self.kb)

        self.answer_chain: Optional[dspy.ChainOfThought] = None
        self.transfer_chain: Optional[dspy.ChainOfThought] = None

        if self.api_key and self.model:
            self._configure_dspy()
        else:
            print("Modo fallback: sin LLM, usando solo FAQ")

    def _configure_dspy(self) -> None:
        """Configurar DSPy con el proveedor de IA."""

        try:
            lm_kwargs = {
                "model": self.model,
                "api_key": self.api_key,
            }
            if self.api_base:
                lm_kwargs["api_base"] = self.api_base

            lm = dspy.LM(**lm_kwargs)
            dspy.settings.configure(lm=lm)

            self.answer_chain = dspy.ChainOfThought(CustomerServiceSignature)
            self.transfer_chain = dspy.ChainOfThought(
                TransferDecisionSignature)

            api_base_info = f" (API base: {self.api_base})" if self.api_base else ""
            print(
                f"DSPy configurado con modelo: {self.model}{api_base_info}")
        except Exception as exc:
            print(f"Error al configurar DSPy: {exc}")
            print("Ejecutandose en modo fallback (solo FAQ)")
            self.answer_chain = None
            self.transfer_chain = None

    def _try_generate_answer(
        self,
        context: str,
        question: str,
        fallback_answer: str,
    ) -> Tuple[str, Optional[Exception]]:
        if not self.answer_chain:
            return fallback_answer, None

        try:
            prediction = self.answer_chain(
                question=question,
                retrieved_passages=context,
            )
            structured_answer = self._compose_structured_answer(prediction)
            return structured_answer or fallback_answer, None
        except Exception as exc:
            return fallback_answer, exc

    @staticmethod
    def _compose_structured_answer(prediction: dspy.Prediction) -> str:
        segments = [
            getattr(prediction, "saludo_y_reconocimiento", ""),
            getattr(prediction, "respuesta_directa", ""),
            getattr(prediction, "proxima_accion_sugerida", ""),
        ]
        return " ".join(
            segment.strip() for segment in segments if isinstance(segment, str) and segment.strip()
        )

    def _handle_llm_failure(
        self,
        result: ChatResult,
        question: str,
        error: Exception,
        agent_context: Dict[str, str],
    ) -> ChatResult:
        error_message = str(error)
        print(f"Error al procesar con LLM: {error_message}")

        error_kind = self._categorize_llm_error(error_message)
        technical_reason = self._technical_reason_for_kind(error_kind)

        enriched_context = dict(agent_context)
        enriched_context["error"] = error_message

        return self._trigger_transfer(
            result=result,
            question=question,
            reason_kind=error_kind,
            technical_reason=technical_reason,
            agent_context=enriched_context,
        )

    def _trigger_transfer(
        self,
        result: ChatResult,
        question: str,
        reason_kind: str,
        technical_reason: str,
        agent_context: Optional[Dict[str, str]] = None,
    ) -> ChatResult:
        result.transfer_to_agent = True
        result.transfer_reason = technical_reason
        result.answer = TRANSFER_MESSAGES.get(
            reason_kind, TRANSFER_MESSAGES["generic"])
        result.source = "transfer"

        self._simulate_transfer(
            question=question,
            reason=technical_reason,
            agent_context=agent_context or {},
        )

        return result

    @staticmethod
    def _categorize_llm_error(message: str) -> str:
        lowered = message.lower()

        if "rate limit" in lowered or "429" in lowered:
            return "rate_limit"
        if "unauthorized" in lowered or "invalid api key" in lowered or "401" in lowered:
            return "auth"
        if "timeout" in lowered or "timed out" in lowered:
            return "timeout"
        if "connection" in lowered or "network" in lowered:
            return "network"
        return "generic"

    @staticmethod
    def _technical_reason_for_kind(kind: str) -> str:
        mapping = {
            "rate_limit": "Limite de velocidad excedido en servicio de IA",
            "auth": "Error de autenticacion con proveedor de IA",
            "timeout": "Tiempo de respuesta agotado al consultar la IA",
            "network": "Incidencia de red al consultar servicio de IA",
            "generic": "Fallo inesperado al generar respuesta con IA",
            "no_answer": "No se encontro informacion relevante en la base de conocimientos",
            "llm_transfer": "El modelo recomienda atencion humana",
        }
        return mapping.get(kind, mapping["generic"])

    def forward(self, question: str) -> Dict[str, str]:
        return self.answer(question)

    def answer(self, question: str) -> Dict[str, str]:
        result = ChatResult(question)
        retrieval = self.retriever(question)
        passages = getattr(retrieval, "passages", [])
        faq_match = getattr(retrieval, "metadata", None)

        if not faq_match and self._is_small_talk(question):
            result.answer = self._small_talk_reply(question)
            result.source = "small_talk"
            return result.to_dict()

        if faq_match:
            result = self._handle_faq_found(
                result,
                question,
                passages,
                faq_match,
            )
        else:
            result = self._handle_faq_not_found(
                result,
                question,
                passages,
            )

        return result.to_dict()

    def _handle_faq_found(
        self,
        result: ChatResult,
        question: str,
        passages: Sequence[str],
        search_result: Dict[str, str],
    ) -> ChatResult:
        category = search_result.get("categoria", "FAQ")
        default_answer = search_result.get("respuesta", "")
        context = "\n\n".join(passages)

        result.source = f"FAQ - Categoria: {category}"
        result.transfer_to_agent = False
        result.transfer_reason = ""

        answer, error = self._try_generate_answer(
            context=context,
            question=question,
            fallback_answer=default_answer,
        )

        result.answer = answer or default_answer

        if error:
            agent_context = {
                "pregunta_relacionada": search_result.get("pregunta", ""),
                "categoria": category,
                "respuesta_sugerida": default_answer,
            }
            return self._handle_llm_failure(
                result=result,
                question=question,
                error=error,
                agent_context=agent_context,
            )

        if self.transfer_chain:
            try:
                transfer_prediction = self.transfer_chain(
                    question=question,
                    retrieved_passages=context or "sin_resultados",
                    generated_answer=result.answer or default_answer,
                )
                should_transfer = self._parse_transfer_decision(
                    transfer_prediction.should_transfer,
                )
            except Exception as error:
                agent_context = {
                    "pregunta_relacionada": search_result.get("pregunta", ""),
                    "categoria": category,
                    "contexto": "fallo en pipeline de transferencia",
                }
                return self._handle_llm_failure(
                    result=result,
                    question=question,
                    error=error,
                    agent_context=agent_context,
                )

            if should_transfer:
                model_reason = getattr(transfer_prediction, "reason", None)
                reason_text = model_reason or self._technical_reason_for_kind(
                    "llm_transfer")
                agent_context = {
                    "pregunta_relacionada": search_result.get("pregunta", ""),
                    "categoria": category,
                    "respuesta_llm": result.answer,
                    "razon_modelo": model_reason,
                }
                return self._trigger_transfer(
                    result=result,
                    question=question,
                    reason_kind="llm_transfer",
                    technical_reason=reason_text,
                    agent_context=agent_context,
                )

        return result

    def _handle_faq_not_found(
        self,
        result: ChatResult,
        question: str,
        passages: Sequence[str],
    ) -> ChatResult:
        result.answer = ""
        result.source = "LLM" if self.answer_chain else "transfer"
        result.transfer_to_agent = False
        result.transfer_reason = ""

        if self.answer_chain:
            context = "\n\n".join(passages) if passages else (
                "No hay informacion relevante en la base de conocimientos para esta pregunta. "
                "Ofrece una respuesta breve y util basada en tu conocimiento general."
            )

            answer, error = self._try_generate_answer(
                context=context,
                question=question,
                fallback_answer="",
            )

            if error:
                agent_context = {
                    "question": question,
                    "contexto": "sin resultados en la base de conocimiento",
                }
                return self._handle_llm_failure(
                    result=result,
                    question=question,
                    error=error,
                    agent_context=agent_context,
                )

            if answer.strip():
                result.answer = answer
                result.source = "LLM"
            else:
                return self._trigger_transfer(
                    result=result,
                    question=question,
                    reason_kind="no_answer",
                    technical_reason=self._technical_reason_for_kind(
                        "no_answer"),
                    agent_context={
                        "question": question,
                        "contexto": "llm_sin_contenido",
                    },
                )

            if self.transfer_chain:
                try:
                    transfer_prediction = self.transfer_chain(
                        question=question,
                        retrieved_passages=context if context else "sin_resultados",
                        generated_answer=result.answer or "",
                    )
                    should_transfer = self._parse_transfer_decision(
                        transfer_prediction.should_transfer,
                    )
                except Exception as error:
                    agent_context = {
                        "question": question,
                        "contexto": "fallo en pipeline de transferencia",
                    }
                    return self._handle_llm_failure(
                        result=result,
                        question=question,
                        error=error,
                        agent_context=agent_context,
                    )

                if should_transfer and not self._is_small_talk(question):
                    model_reason = getattr(transfer_prediction, "reason", None)
                    reason_text = model_reason or self._technical_reason_for_kind(
                        "llm_transfer")
                    agent_context = {
                        "question": question,
                        "respuesta_llm": result.answer,
                        "razon_modelo": model_reason,
                    }
                    return self._trigger_transfer(
                        result=result,
                        question=question,
                        reason_kind="llm_transfer",
                        technical_reason=reason_text,
                        agent_context=agent_context,
                    )

            return result

        if self._is_small_talk(question):
            result.answer = self._small_talk_reply(question)
            result.source = "small_talk"
            result.transfer_to_agent = False
            result.transfer_reason = ""
            return result

        return self._trigger_transfer(
            result=result,
            question=question,
            reason_kind="no_answer",
            technical_reason=self._technical_reason_for_kind("no_answer"),
            agent_context={
                "question": question,
                "contexto": "sin_coincidencias_faq",
            },
        )

    def _parse_transfer_decision(self, decision_text: str) -> bool:
        decision_lower = (decision_text or "").strip().lower()
        return decision_lower in {"si", "si", "yes", "true", "si.", "si.", "yes."}

    def _simulate_transfer(
        self,
        question: str,
        reason: str,
        agent_context: Dict[str, str],
    ) -> None:
        print("\n" + "=" * 60)
        print("TRANSFERENCIA A AGENTE HUMANO")
        print("=" * 60)
        print(f"Pregunta original: {question}")
        print(f"Motivo tecnico: {reason}")

        if agent_context:
            print("-" * 60)
            print("Contexto sugerido para el agente:")
            for key, value in agent_context.items():
                if value is None:
                    continue
                printable = self._truncate_for_agent(str(value))
                if printable:
                    print(f"- {key}: {printable}")

        print("-" * 60)
        print("Estado: Conectando con agente disponible...")
        print("Tiempo estimado de espera: 2-3 minutos")
        print("=" * 60 + "\n")

    @staticmethod
    def _truncate_for_agent(text: str) -> str:
        clean_text = " ".join(text.split())
        limit = AGENT_CONTEXT_LIMIT
        if len(clean_text) > limit:
            return clean_text[:limit].rstrip() + "..."
        return clean_text

    @staticmethod
    def _is_small_talk(question: str) -> bool:
        normalized = question.lower().strip()
        if normalized in SMALL_TALK_PHRASES:
            return True
        return len(normalized) <= 20 and any(
            normalized.startswith(prefix) for prefix in SMALL_TALK_PREFIXES
        )

    @staticmethod
    def _small_talk_reply(question: str) -> str:
        base_reply = (
            "Hola! Estoy aqui para ayudarte con todo lo relacionado a Grupo Lazarus. "
            "En que puedo asistirte hoy?"
        )
        if "grac" in question.lower():
            return "Con gusto! Si necesitas algo mas sobre Grupo Lazarus, dime"
        return base_reply


__all__ = ["LazarusChatbot"]
