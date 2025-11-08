## Instantánea del Proyecto
- Chatbot RAG para Grupo Lazarus en Python 3.13; DSPy orquesta modelos de OpenRouter cuando `OPENROUTER_API_KEY` está disponible, de lo contrario responde con las FAQ sin LLM.
- El devcontainer ya trae Python, pip y dependencias del `requirements.txt`; no se utiliza intérprete virtual (`venv` o similar), ejecuta todo con el `python` global del contenedor.
- `faq_grupo_lazarus.xlsx` debe vivir en la raíz; si falta, `FAQKnowledgeBase.load_data()` lanza `FileNotFoundError` y todo flujo que invoque al bot fallará.
- `chatbot.py` ofrece chat interactivo y `ejemplo.py` ejecuta smoke tests (FAQ directas, transferencia simulada, uso de modelo personalizado).

## Módulos Clave
- `chatbot.LazarusChatbot` combina la búsqueda en FAQ con instancias DSPy `ChainOfThought`; mantén la bifurcación entre camino con LLM y modo fallback sin modelo.
- `answer()` entrega un diccionario con `question`, `answer`, `source`, `transfer_to_agent` y `transfer_reason`; cualquier clave nueva exige actualizar a los consumidores (`ejemplo.py`, integraciones futuras).
- `_simulate_transfer()` sólo imprime el traspaso; si se reemplaza, conserva tono conversacional y la bandera `transfer_to_agent` para que `chatbot.chat()` cierre bien.
- `rag_knowledge_base.FAQKnowledgeBase` carga las FAQ una vez y expone `search`, `get_all_faqs` y `get_faqs_by_category`; reutiliza estas APIs antes de leer el Excel directamente.

## Base de Conocimiento y ETL
- El Excel original usa columnas `Pregunta`, `Respuesta`, `Categoría`; el notebook `notebooks/demo_etl.ipynb` las normaliza a snake_case sin ascentos (`df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')`) y genera `faq_limpio.csv`.
- `search()` elimina stopwords en español, normaliza sinónimos de ubicación (`donde`, `direccion`, etc. → `ubicad`) y evalúa coincidencias parciales con umbral 0.2; ajusta pesos sólo con pruebas que validen la pertinencia.
- Para nuevas categorías, apóyate en `get_faqs_by_category` en lugar de filtrar listas manualmente para mantener consistencia.
- Si incorporas otras fuentes, replica los pasos del notebook: `fillna` en `respuesta`, limpieza de espacios y `drop_duplicates` por pregunta/respuesta.

## Flujos de Trabajo
- Carga variables de entorno con `dotenv.load_dotenv()` antes de crear `LazarusChatbot`; tanto `chatbot.py` como `ejemplo.py` ilustran el patrón.
- Configura DSPy una sola vez por proceso; inicializaciones repetidas cambian `dspy.settings`, así que reutiliza la instancia del bot en servicios persistentes.
- `python ejemplo.py` funciona como regresión rápida: comprueba respuestas conocidas, transferencia y el manejo de modelos según API key.
- Para QA manual, ejecuta `python chatbot.py` y valida respuestas de FAQ y el mensaje de transferencia cuando la pregunta no está cubierta.

## Convenciones
- Las respuestas incluyen texto en español con emojis; conserva ese estilo en cualquier nuevo output visible para usuarios.
- Evita rutas absolutas: usa parámetros (`excel_file`) o constantes ya definidas cuando abras datos.
- Todas las dependencias se gestionan desde `requirements.txt`; si agregas librerías verifica que se instalen en el devcontainer base sin pasos extra.
- Cuando transformes datos en pandas, adopta el patrón del notebook para asegurar compatibilidad con el cargador de FAQ.

## Extensión Segura
- Si mejoras la recuperación, amplía `FAQKnowledgeBase` en vez de saltarte su lógica de stopwords y sinónimos.
- Cualquier feature nuevo que dependa de OpenRouter debe degradar con el mismo aviso utilizado actualmente cuando `self.api_key` está ausente.
- Para decisiones automáticas de transferencia, reutiliza `TransferDecisionSignature` y la infraestructura Chain-of-Thought ya definida.
- Documenta nuevos flujos o contratos de datos aquí o en `README.md` para que otros agentes los adopten de inmediato.
