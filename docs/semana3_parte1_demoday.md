# Equipos Técnicos (Foco: Código, Implementación y Datos)

## 1. Equipo 1 (Forecast): Implementación de AutoTS
- **Archivos/Código Clave**: Scripts principales como `pipeline_autots.py` y `model_saver.py`. Se genera un log de ejecución (`model_selection.log`) y los modelos guardados se almacenan como archivos serializados (.pkl) en la carpeta `artefactos/forecast/`.
- **Funcionamiento General**: Se implementó el flujo de carga de datos y filtrado de reglas de negocio. El código itera, ejecuta AutoTS para la selección automática del modelo, y el modelo con el mejor desempeño (menor MSE) es guardado (serializado) en el repositorio para su uso futuro sin reentrenamiento.
- **Artefacto Final**: Un conjunto de modelos serializados (.pkl) listos para ser cargados y un reporte JSON que mapea cada producto con el ID del modelo ganador.

## 2. Equipo 2 (Chatbot): Desarrollo v1.0 y Medición
- **Archivos/Código Clave**: Componentes principales como `chatbot_v1.0.py` (lógica del agente), `vector_db_chroma.py` (manejo de embeddings) y `metrics_collector.py` (medición).
- **Funcionamiento General**: El pipeline del chatbot (RAG) está funcional. El código genera embeddings de las preguntas, recupera el contexto relevante de la base de datos interna (ej. ChromaDB) y lo inyecta al LLM para la respuesta. Se ha integrado el código para la medición de la latencia en cada consulta.
- **Artefacto Final**: Un funcionamiento consola o un endpoint API (`/ask_agent`) funcional y un registro de métricas que indica el tiempo de respuesta promedio del agente.

# Equipos no Técnicos (Foco: Valor, KPIs y Experiencia)

## 3. Equipo 3 (Forecast): Análisis y Valor
- **Documentos Clave**: Se generó `Reporte_Ejecutivo_Valor_Forecast.pdf` y un archivo/imagen de diagrama.
- **Funcionamiento General**: Se definió la propuesta de valor del MVP de AutoTS, estableciendo 3 características clave del negocio (ej. ROI, reducción de stockouts). Se completó el análisis del proceso y de la competencia. El principal resultado es la creación de un diagrama que muestra el flujo de trabajo deseado con el modelo automático, contrastándolo con el proceso manual.
- **Artefacto Final**: El Reporte Ejecutivo que define las métricas de negocio para la evaluación (KPIs) y el diagrama de flujo de proceso que guía la implementación del MVP.

## 4. Equipo 4 (Chatbot): UX, Persona y Pruebas de Robustez
- **Documentos Clave**: Se entregó `Documento_Persona_Lazarus.pdf` y la matriz de pruebas de robustez (`10_Preguntas_Imposibles.xlsx`).
- **Funcionamiento General**: Se completó el análisis de la Experiencia de Usuario (UX), enfocándose en cómo el agente maneja errores y la escalada humana. Se definió la Persona de Lázarus (tono, frases de inicio/cierre). Se crearon 10 test cases negativos para probar la robustez del código, asegurando que el agente no invente respuestas.
- **Artefacto Final**: El documento de la Persona que estandariza la comunicación y la matriz de pruebas con los 10 escenarios negativos, listos para ser ejecutados contra la Versión 1.0.