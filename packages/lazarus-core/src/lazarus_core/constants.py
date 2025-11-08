"""Constantes compartidas para el paquete chatbot."""

SMALL_TALK_PHRASES = {
    "hola",
    "hola!",
    "hola.",
    "buenas",
    "buenas!",
    "buenas tardes",
    "buenas noches",
    "buenos dias",
    "buenos dias",
    "hey",
    "que tal",
    "que tal",
    "gracias",
    "muchas gracias",
    "ok",
    "vale",
    "entendido",
    "perfecto",
    "hola chatbot",
    "hola bot",
    "hola lazarus",
}

SMALL_TALK_PREFIXES = (
    "hola",
    "buen",
    "grac",
    "hey",
    "que tal",
    "que tal",
)

TRANSFER_MESSAGES = {
    "no_answer": (
        "Lo siento, no tengo informacion especifica sobre esa pregunta en mi base de datos. "
        "Voy a transferir su consulta a uno de nuestros agentes especializados que podra ayudarle mejor."
    ),
    "rate_limit": (
        "Nuestra IA esta atendiendo muchas consultas en este momento y no pudo responder a tiempo. "
        "Te conecto con un agente humano para continuar."
    ),
    "timeout": (
        "La IA tardo mas de lo esperado en responder. Derivare tu caso a un agente humano para que recibas ayuda inmediata."
    ),
    "auth": (
        "No pude autenticarme con el servicio de IA. Permiteme transferirte con un agente humano para resolverlo contigo."
    ),
    "network": (
        "Tuvimos un inconveniente de conexion con el servicio de IA. Enseguida te enlazo con un agente humano que pueda ayudarte."
    ),
    "generic": (
        "Ocurrio un imprevisto al generar la respuesta automatica. Te conectare con un agente humano para continuar."
    ),
    "llm_transfer": (
        "Para darte una respuesta mas precisa, compartire tu consulta con uno de nuestros agentes especialistas. En un momento se pondra en contacto contigo!"
    ),
}

AGENT_CONTEXT_LIMIT = 220
