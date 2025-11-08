"""
Ejemplo de uso del Chatbot Lazarus
Demuestra varias características incluyendo RAG y transferencia de agente
"""

from lazarus_core import LazarusChatbot
from dotenv import load_dotenv
import os


def example_without_llm():
    """Ejemplo 1: Uso básico del chatbot (sin LLM)"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Uso Básico del Chatbot (Sin LLM)")
    print("="*60 + "\n")

    # Instanciar el chatbot
    chatbot = LazarusChatbot()

    # Pregunta de prueba
    question = "¿Cuál es el horario de atención?"

    print(f"Pregunta: {question}")
    response = chatbot.answer(question)
    print(f"Respuesta: {response['answer']}")
    print(f"Fuente: {response['source']}")
    print("-" * 60 + "\n")


def example_with_llm():
    """Ejemplo 2: Uso con DSPy genérico (con LLM)"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Uso con DSPy Genérico (Con LLM)")
    print("="*60 + "\n")

    api_key = os.getenv("DSPY_API_KEY")
    model = os.getenv("DSPY_MODEL")
    api_base = os.getenv("DSPY_API_BASE")

    if api_key and api_key != "your_api_key_here" and model:
        config_info = f"API Key: {api_key[:20]}..., Modelo: {model}"
        if api_base:
            config_info += f", Gateway: {api_base}"
        print(f"Configuración detectada: {config_info}\n")

        chatbot = LazarusChatbot(api_key=api_key, model=model)

        question = "¿Tienen garantía?"
        print(f"Pregunta: {question}")
        response = chatbot.answer(question)
        print(f"Respuesta: {response['answer']}")
        print(f"Fuente: {response['source']}")
    else:
        print(
            "⚠ Configuración incompleta. Define en .env:\n"
            "  - DSPY_API_KEY (API key del proveedor)\n"
            "  - DSPY_MODEL (formato: provider/model-name, ej: openai/gpt-3.5-turbo)\n"
            "  - DSPY_API_BASE (opcional, para gateways personalizados)"
        )

    print("-" * 60 + "\n")


def main():
    """Ejecutar todos los ejemplos"""
    # Cargar variables de entorno
    load_dotenv()

    print("\n")
    print("*" * 60)
    print("  EJEMPLOS DE USO - Chatbot Grupo Lazarus")
    print("*" * 60)

    # Ejecutar los ejemplos
    example_without_llm()
    example_with_llm()

    print("\n" + "="*60)
    print("Para iniciar el chatbot interactivo, ejecute:")
    print("  python -m lazarus_apps.main")
    print("\nPara usar la interfaz Streamlit, ejecute:")
    print("  streamlit run src/lazarus_apps/ui.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
