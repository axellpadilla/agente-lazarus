"""
Chatbot Agent using DSPy and OpenRouter API
Implements RAG-based question answering with agent transfer simulation
"""

import os
from typing import Optional, Dict
import dspy
from rag_knowledge_base import FAQKnowledgeBase


class RAGSignature(dspy.Signature):
    """Signature for RAG-based question answering"""
    context = dspy.InputField(desc="Relevant context from knowledge base")
    question = dspy.InputField(desc="User's question")
    answer = dspy.OutputField(desc="Answer based on the context")


class TransferDecisionSignature(dspy.Signature):
    """Signature for deciding if question needs agent transfer"""
    question = dspy.InputField(desc="User's question")
    search_result = dspy.InputField(desc="Result from knowledge base search")
    should_transfer = dspy.OutputField(desc="Whether to transfer to human agent (Si/No)")
    reason = dspy.OutputField(desc="Reason for the decision")


class LazarusChatbot:
    """
    Intelligent chatbot for Grupo Lazarus
    Uses RAG to answer questions from FAQ database
    Transfers to human agent when information is not found
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "openai/gpt-3.5-turbo",
        excel_file: str = "faq_grupo_lazarus.xlsx"
    ):
        """
        Initialize the chatbot
        
        Args:
            api_key: OpenRouter API key (or set OPENROUTER_API_KEY env var)
            model: Model to use (default: openai/gpt-3.5-turbo)
            excel_file: Path to FAQ Excel file
        """
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            print("⚠ Warning: No API key provided. Set OPENROUTER_API_KEY environment variable.")
            print("⚠ Running in demo mode with limited functionality.")
        
        # Initialize knowledge base
        self.kb = FAQKnowledgeBase(excel_file)
        
        # Configure DSPy with OpenRouter
        if self.api_key:
            try:
                lm = dspy.OpenAI(
                    model=model,
                    api_key=self.api_key,
                    api_base="https://openrouter.ai/api/v1",
                    model_type="chat"
                )
                dspy.settings.configure(lm=lm)
                self.rag_module = dspy.ChainOfThought(RAGSignature)
                self.transfer_module = dspy.ChainOfThought(TransferDecisionSignature)
                print(f"✓ DSPy configured with model: {model}")
            except Exception as e:
                print(f"⚠ Error configuring DSPy: {e}")
                print("⚠ Running in fallback mode")
                self.rag_module = None
                self.transfer_module = None
        else:
            self.rag_module = None
            self.transfer_module = None
    
    def answer(self, question: str) -> Dict[str, any]:
        """
        Answer a user question using RAG
        
        Args:
            question: User's question
        
        Returns:
            Dictionary with answer, source, and transfer status
        """
        # Search knowledge base
        search_result = self.kb.search(question)
        
        # Prepare response
        response = {
            "question": question,
            "answer": "",
            "source": "knowledge_base",
            "transfer_to_agent": False,
            "transfer_reason": ""
        }
        
        if search_result:
            # Found relevant information
            if self.rag_module:
                # Use DSPy to generate contextual answer
                try:
                    context = f"Pregunta relacionada: {search_result['pregunta']}\nRespuesta: {search_result['respuesta']}"
                    result = self.rag_module(context=context, question=question)
                    response["answer"] = result.answer
                except Exception as e:
                    # Fallback to direct answer
                    response["answer"] = search_result['respuesta']
            else:
                # Fallback mode - use direct answer
                response["answer"] = search_result['respuesta']
            
            response["source"] = f"FAQ - Categoría: {search_result['categoria']}"
        else:
            # No relevant information found
            response["transfer_to_agent"] = True
            response["transfer_reason"] = "No se encontró información relevante en la base de conocimientos"
            response["answer"] = (
                "Lo siento, no tengo información específica sobre esa pregunta en mi base de datos. "
                "Voy a transferir su consulta a uno de nuestros agentes especializados que podrá ayudarle mejor."
            )
            response["source"] = "transfer"
            
            # Simulate transfer
            self._simulate_transfer(question)
        
        return response
    
    def _simulate_transfer(self, question: str) -> None:
        """
        Simulate transfer to human agent
        
        Args:
            question: Question that triggered the transfer
        """
        print("\n" + "="*60)
        print("🔄 TRANSFERENCIA A AGENTE HUMANO")
        print("="*60)
        print(f"Pregunta: {question}")
        print("Estado: Conectando con agente disponible...")
        print("Tiempo estimado de espera: 2-3 minutos")
        print("="*60 + "\n")
    
    def chat(self) -> None:
        """Start interactive chat session"""
        print("\n" + "="*60)
        print("💬 Chatbot Grupo Lazarus")
        print("="*60)
        print("Hola! Soy el asistente virtual de Grupo Lazarus.")
        print("Puedo responder preguntas sobre nuestros servicios, horarios,")
        print("ubicación, políticas y más.")
        print("\nEscribe 'salir' para terminar la conversación.")
        print("="*60 + "\n")
        
        while True:
            try:
                question = input("Tú: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['salir', 'exit', 'quit', 'adios']:
                    print("\nChatbot: ¡Hasta luego! Que tenga un excelente día.")
                    break
                
                # Get answer
                response = self.answer(question)
                
                print(f"\nChatbot: {response['answer']}")
                print(f"(Fuente: {response['source']})\n")
                
                # If transfer was triggered, break the loop
                if response['transfer_to_agent']:
                    print("La conversación será transferida a un agente humano.\n")
                    break
                
            except KeyboardInterrupt:
                print("\n\nChatbot: ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}\n")


def main():
    """Main function to run the chatbot"""
    # Initialize chatbot
    chatbot = LazarusChatbot()
    
    # Start chat session
    chatbot.chat()


if __name__ == "__main__":
    main()
