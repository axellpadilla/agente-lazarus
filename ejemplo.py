"""
Example usage of the Lazarus Chatbot
Demonstrates various features including RAG and agent transfer
"""

from chatbot import LazarusChatbot
from dotenv import load_dotenv
import os


def example_basic_usage():
    """Example 1: Basic chatbot usage"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Uso Básico del Chatbot")
    print("="*60 + "\n")
    
    # Load environment variables
    load_dotenv()
    
    # Create chatbot instance
    chatbot = LazarusChatbot()
    
    # Test questions
    test_questions = [
        "¿Cuál es el horario de atención?",
        "¿Dónde están ubicadas las oficinas?",
        "¿Qué servicios ofrecen?",
    ]
    
    for question in test_questions:
        print(f"Pregunta: {question}")
        response = chatbot.answer(question)
        print(f"Respuesta: {response['answer']}")
        print(f"Fuente: {response['source']}")
        print("-" * 60 + "\n")


def example_transfer_scenario():
    """Example 2: Scenario that triggers agent transfer"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Escenario de Transferencia a Agente")
    print("="*60 + "\n")
    
    load_dotenv()
    chatbot = LazarusChatbot()
    
    # Question not in knowledge base
    unknown_question = "¿Puedo personalizar el color del producto?"
    
    print(f"Pregunta: {unknown_question}")
    response = chatbot.answer(unknown_question)
    print(f"Respuesta: {response['answer']}")
    print(f"Transferir a agente: {response['transfer_to_agent']}")
    if response['transfer_to_agent']:
        print(f"Razón: {response['transfer_reason']}")
    print("-" * 60 + "\n")


def example_custom_model():
    """Example 3: Using a custom model"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Uso con Modelo Personalizado")
    print("="*60 + "\n")
    
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if api_key and api_key != "your_api_key_here":
        # Use GPT-4 for better responses
        chatbot = LazarusChatbot(
            api_key=api_key,
            model="openai/gpt-4"
        )
        
        question = "¿Tienen garantía?"
        print(f"Pregunta: {question}")
        response = chatbot.answer(question)
        print(f"Respuesta: {response['answer']}")
        print(f"Fuente: {response['source']}")
    else:
        print("⚠ API key no configurada. Configure OPENROUTER_API_KEY en .env")
    
    print("-" * 60 + "\n")


def example_knowledge_base_inspection():
    """Example 4: Inspecting the knowledge base"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Inspección de la Base de Conocimientos")
    print("="*60 + "\n")
    
    from rag_knowledge_base import FAQKnowledgeBase
    
    kb = FAQKnowledgeBase()
    
    print(f"Total de FAQs cargadas: {len(kb.get_all_faqs())}")
    print("\nCategorías disponibles:")
    categories = set(faq['categoria'] for faq in kb.get_all_faqs())
    for cat in sorted(categories):
        count = len(kb.get_faqs_by_category(cat))
        print(f"  - {cat}: {count} preguntas")
    
    print("\nEjemplo de FAQ:")
    if kb.get_all_faqs():
        faq = kb.get_all_faqs()[0]
        print(f"  Pregunta: {faq['pregunta']}")
        print(f"  Respuesta: {faq['respuesta'][:100]}...")
        print(f"  Categoría: {faq['categoria']}")
    
    print("-" * 60 + "\n")


def main():
    """Run all examples"""
    print("\n")
    print("*" * 60)
    print("  EJEMPLOS DE USO - Chatbot Grupo Lazarus")
    print("*" * 60)
    
    # Run examples
    example_knowledge_base_inspection()
    example_basic_usage()
    example_transfer_scenario()
    example_custom_model()
    
    print("\n" + "="*60)
    print("Para iniciar el chatbot interactivo, ejecute:")
    print("  python chatbot.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
