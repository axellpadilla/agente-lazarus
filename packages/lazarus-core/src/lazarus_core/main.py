from dotenv import load_dotenv

from .bot import LazarusChatbot


def main() -> None:
    """Punto de entrada de linea de comandos para el chatbot."""

    load_dotenv()
    LazarusChatbot().chat()


if __name__ == "__main__":
    main()
