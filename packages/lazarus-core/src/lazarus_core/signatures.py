"""Firmas de DSPy utilizadas por el chatbot Lazarus."""

import dspy


class CustomerServiceSignature(dspy.Signature):
    """Genera una respuesta estructurada para la atencion al cliente."""

    question = dspy.InputField(desc="Pregunta original del cliente.")
    retrieved_passages = dspy.InputField(
        desc=(
            "Pasajes recuperados desde la base de conocimientos que deben usarse como"
            " evidencia principal."
        )
    )

    saludo_y_reconocimiento = dspy.OutputField(
        desc="Saludo formal y reconocimiento de la consulta."
    )
    respuesta_directa = dspy.OutputField(
        desc="Respuesta concisa sustentada en el contexto recuperado."
    )
    proxima_accion_sugerida = dspy.OutputField(
        desc="Pasos siguientes o recomendaciones adicionales para la persona usuaria."
    )


class TransferDecisionSignature(dspy.Signature):
    """Determina si se debe transferir la conversacion a un agente humano."""

    question = dspy.InputField(desc="Pregunta del usuario")
    retrieved_passages = dspy.InputField(
        desc="Resumen del resultado de busqueda o motivo de ausencia de contexto."
    )
    generated_answer = dspy.InputField(
        desc="Respuesta propuesta por la IA para evaluar si es suficiente."
    )
    should_transfer = dspy.OutputField(
        desc="Indica si se recomienda transferir (si/no)."
    )
    reason = dspy.OutputField(desc="Justificacion breve de la recomendacion.")
