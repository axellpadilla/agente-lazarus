## Instantánea del Proyecto
- Chatbot RAG para Grupo Lazarus en Python 3.13; DSPy orquesta modelos de cualquier proveedor compatible (OpenAI, Anthropic, etc.) según configuración genérica en variables de entorno; fallback a FAQ sin LLM si no están configuradas.
- El devcontainer usa **`uv` (Astral)** como gestor de paquetes; `.devcontainer/postcreate.sh` verifica Python 3.13, instala `uv`, descarga dependencias, valida archivos críticos y corre un smoke test.
- `data_limpia/faq_limpio.csv` es la fuente primaria para el bot; el Excel crudo (`faq_grupo_lazarus.xlsx`) se usa en procesos ETL y debe existir para regenerar el CSV.
- `python -m lazarus_apps.main` inicia el chat interactivo; `python ejemplo.py` corre smoke tests (FAQ directas, transferencia simulada, uso de modelo con/fallback).

## Módulos Clave
- `lazarus_core.LazarusChatbot` encapsula todo el flujo DSPy: `FAQRetriever` (recuperación), `CustomerServiceSignature` (respuesta estructurada), `TransferDecisionSignature` (decisión de transferencia) y `ChatResult` como contrato de salida.
- `answer()` devuelve un diccionario con `question`, `answer`, `source`, `transfer_to_agent` y `transfer_reason`; cualquier cambio requiere sincronizar consumidores (`ejemplo.py`, integraciones externas).
- `_compose_structured_answer()` concatena saludo, respuesta directa y próxima acción; respeta el estilo con emojis y tono cordial.
- `_simulate_transfer()` imprime la simulación para QA; si migras a integración real, conserva el estado `transfer_to_agent=True` para cerrar la conversación correctamente.
- `lazarus_core.retriever.FAQRetriever` reusa `lazarus_kb.FAQKnowledgeBase.search()` pero entrega pasajes compatibles con DSPy.
- `lazarus_kb.FAQKnowledgeBase` sigue siendo la fuente de verdad; preferir sus métodos `search`, `get_all_faqs`, `get_faqs_by_category`.

## Base de Conocimiento y ETL
- El Excel original usa columnas `Pregunta`, `Respuesta`, `Categoría`; el notebook `notebooks/demo_etl.ipynb` las normaliza a snake_case (sin acentos) y genera `data_limpia/faq_limpio.csv`.
- `FAQKnowledgeBase.search()` quita stopwords en español, unifica sinónimos de ubicación (`donde`, `direccion`, `ubicacion` → `ubicad`) y evalúa coincidencias parciales (umbral 0.2).
- Apóyate en `get_faqs_by_category` y `get_all_faqs`; evita leer el CSV directamente desde otras partes del código.
- Si agregas fuentes externas, replica el pipeline del notebook (`fillna` en `respuesta`, `strip`, `drop_duplicates` por pregunta/respuesta) antes de fusionarlas.

## Flujos de Trabajo
- Carga variables de entorno con `dotenv.load_dotenv()` antes de instanciar `LazarusChatbot`; `src/lazarus_apps/main.py`, `ejemplo.py` muestran la pauta.
- Variables de entorno requeridas: `DSPY_API_KEY` y `DSPY_MODEL` (formato: `gateway/provider/model-name`). Opcional: `DSPY_API_BASE` para gateways personalizados.
- El devcontainer lanza `.devcontainer/postcreate.sh` tras crearse: valida Python, instala `uv`, descarga dependencias y .venv con `uv sync`, verifica archivos críticos y corre un smoke test con `python ejemplo.py`.
- Para instalación local o nuevas dependencias, usa `uv add <package> --project <project name>` (más rápido y determinista). Evita `pip install` directo.
- Configura DSPy una sola vez por proceso (`dspy.settings.configure(lm=...)` en `_configure_dspy`); reutiliza la instancia para hilos/servicios persistentes.
- `python ejemplo.py` sigue siendo la regresión rápida: cubre respuestas conocidas, transferencia automática y selección de modelo según API key.
- Para QA manual del chat, ejecuta `python -m lazarus_apps.main` y valida tanto respuestas de FAQ como transferencias.

## Estructura Modular (Workspace uv)
- **lazarus-kb**: Paquete de base de conocimiento (FAQ search).
- **lazarus-core**: Paquete backend (DSPy chatbot, depende de lazarus-kb).
- **lazarus-apps**: Aplicación raíz (CLI + UI Streamlit, depende de lazarus-core).
- Data en `data_limpia/faq_limpio.csv` (compartido).
- Tasks VS Code: `uv-run` y `uv-sync` para ejecutar comandos.

## Convenciones
- Respuestas orientadas al usuario siempre en español y con emojis amigables (seguimos el estilo actual de `ChatResult`).
- Evita rutas absolutas; usa parámetros (`excel_file`) o constantes definidas.
- Gestiona dependencias vía `pyproject.toml` + `uv`; verifica compatibilidad con el devcontainer base antes de añadir librerías.
- Para ETL en pandas, sigue el patrón del notebook (normalización de columnas, `fillna`, `strip`, `drop_duplicates`).

## Extensión Segura
- Si extiendes la recuperación, hazlo a través de `FAQKnowledgeBase` y/o `FAQRetriever` para conservar la normalización de stopwords y el contrato DSPy.
- Las features que dependan de proveedores de IA deben mantener el fallback claro cuando `self.api_key` está ausente (mensajes y modo FAQ literal).
- Usa las firmas existentes (`CustomerServiceSignature`, `TransferDecisionSignature`) al añadir pasos razonadores; si las modificas, actualiza `_compose_structured_answer` y pruebas.
- Documenta nuevos flujos o contratos de datos en este archivo o en `README.md` para mantener alineados a otros agentes.
