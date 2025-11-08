"""Punto de entrada para el CLI del chatbot Lazarus."""

from dotenv import load_dotenv
from lazarus_core import LazarusChatbot


def main() -> None:
    """Punto de entrada de linea de comandos interactivo para el chatbot."""

    load_dotenv()

    print("\n" + "=" * 60)
    print("  CHATBOT GRUPO LAZARUS - Interfaz Interactiva")
    print("=" * 60 + "\n")

    chatbot = LazarusChatbot()

    print("Escriba 'salir' o 'exit' para terminar.\n")

    while True:
        try:
            user_input = input("Tu pregunta: ").strip()

            if user_input.lower() in {"salir", "exit", "quit"}:
                print("\nGracias por usar Lazarus Chatbot. Hasta luego!")
                break

            if not user_input:
                continue

            response = chatbot.answer(user_input)

            print(f"\nRespuesta: {response['answer']}")
            print(f"Fuente: {response['source']}")

            if response.get('transfer_to_agent'):
                print(f"Motivo de transferencia: {response['transfer_reason']}")

            print("-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\nChatbot interrumpido por usuario.")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
