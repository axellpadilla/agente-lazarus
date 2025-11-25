🚀 **Temática Clave — Progreso MVP, Git y Auto-TS**

- **Progreso MVP:** Discusión sobre desafíos en limpieza de datos y exploración de herramientas de benchmarking.
- **Conceptos Técnicos:** Explicación de hiperparámetros, validación cruzada y flujo de trabajo con Git.
- **Configuración de Entorno:** Setup de notebooks para análisis de acciones y uso de `uv` / Python.
- **Organización:** Establecimiento de equipos de trabajo con roles y reprogramación del Demo Day.

## ✅ Conclusiones y Tareas Inmediatas

- **luis.castillo:** Explorar y probar la última versión del código compartido con integración de LLM en la nube.
- **luis.sabillon:** Revisar el código del agente para entender la conexión con LLM y explorar el repositorio pendiente.
- **Nelson:** Completar el análisis de ventajas y desventajas de las herramientas de chatbot investigadas.
- **Todos los participantes:**
  - Elegir un equipo y una tarea específica para el MVP que presentarán en el demo day.
  - Explorar ChatWoot como alternativa de código libre para reemplazar Senvia.
  - Probar el nuevo repositorio actualizado con Auto-TS y completar el pipeline de pronósticos.

## 🧠 Contenido Principal de la Sesión

### Progreso del Proyecto MVP
El equipo discutió el progreso de las tareas asignadas para el proyecto de MVP. Luis Castillo reportó dificultades con la limpieza de datos en el repositorio debido a problemas con el orden de fechas, mientras que Franklin compartió una solución usando funciones para manejar valores nulos. Los participantes exploraron diferentes herramientas de benchmarking incluyendo Zoho, Scendia y ChatGPT, con Nelson presentando un análisis comparativo de opciones como Intercom y Salesforce. Axell explicó los conceptos técnicos de hiperparámetros y validación cruzada, y mencionó que proporcionaría un repositorio actualizado para el desarrollo del MVP.

### Flujo de trabajo con Git
Axell explicó el flujo de trabajo con Git y recomendó borrar y recrear el espacio de trabajo para mantenerse actualizado, especialmente para aquellos que no están familiarizados con Git. Luis Castillo preguntó sobre las ventajas de trabajar directamente en GitHub versus herramientas locales como Visual Studio Code, y Axell respondió que para propósitos locales prefiere el ambiente local ya que se genera automáticamente al clonar el repositorio. Luis Sabillon resolvió su problema al borrar el espacio de trabajo existente y recrearlo nuevo. Axell mencionó que el repositorio actualiza con nuevos cambios de código, incluyendo un nuevo demo completo en los notebooks que muestra todo el pipeline.

### Configuración Python para Análisis Financiero
Axell y luis.sabillon discutieron la configuración de notebooks y paquetes de Python para el análisis de datos de acciones. Axell explicó que el paquete se instala en Python y incluye dependencias como la API de Yahoo Finance, Pandas, Numpy y Auto Ts. El equipo probó el primer segmento del proceso y luis.sabillon confirmó que el análisis de Pire Line se ejecutó correctamente y generó gráficos. Axell mostró el demo completo del proceso, incluyendo la ingesta de datos a través de la API de Yahoo y la preparación de los datos en formato ancho para trabajar con Auto Ts.

### Proceso Auto TS para Datos
Axell explicó el proceso de extracción y transformación de datos de acciones utilizando Auto TS, incluyendo la descarga de datos desde una API y la transformación del formato para prepararlo para el entrenamiento. Discutieron cómo manejar variables como feriados y estacionalidad, donde Luis mencionó que los productos de alta rotación bajan en días feriados mientras que los de baja rotación se venden más en estos días. Axell explicó que la variable más difícil de integrar es cuando los datos están sucios, y mencionó que Auto TS puede automatizar la adición de características como diferencias de días y regresos al futuro.

### Filtrado y Transformación de Datos
Axell explicó que la parte más difícil del proyecto será el filtrado de datos, especialmente porque no todos los productos tienen suficientes datos disponibles. Mencionó que el entrenamiento inicial debe ser lo más simple posible y que el costo principal será extraer la información, no el clima que se puede obtener mediante APIs gratuitas. Axell también describió un concepto complejo donde se predice el mismo producto en diferentes niveles (país y almacén) y los modelos se retroalimentan entre sí, asignando pesos a cada serie según su importancia por nivel. La discusión se centró en el segundo paso del proyecto: la transformación de datos, donde se mencionó la creación de un data set con fechas y la posibilidad de agregar información sobre stock, aunque se necesitaría hacerlo producto por producto para mantener correlaciones fijas.

### Manejo de Inventario con Machine Learning
Axell y Luis discutieron los desafíos del manejo de inventario en el negocio de medicina, donde a veces los productos se retrasan y se generan picos de demanda en meses posteriores como diciembre. Axell explicó cómo el machine learning puede detectar estos patrones y predecirlos, mencionando que Auto Ts busca el mejor modelo para cada serie de productos y genera un template que se puede reutilizar sin tener que entrenar nuevamente el modelo. La conversación se centró en los pasos de entrenamiento del modelo, la generación de predicciones y la importancia de usar templates optimizados para mejorar el rendimiento del sistema.

### Sistema de Predicción Auto-TS
Axell explicó el funcionamiento del sistema de predicción auto-TS, destacando que se selecciona el modelo con menor error y que las acciones no son predecibles, por lo que el sistema se basa en la validación cruzada. Se presentaron cuatro equipos de trabajo: dos técnicos (uno enfocado en forecast y otro en chatbot), uno de negocio y otro de análisis de interfaz de usuario. Cada equipo tiene tareas específicas, como la selección del mejor modelo predictivo, la definición de la identidad del chatbot y la medición de métricas, con el objetivo de iterar y mejorar el sistema progresivamente.

### Reprogramación y Evaluación Demo Day
El equipo discutió los cambios en la programación del Demo Day, que se reprogramó para el 26 y 27 de noviembre, y el 4 de diciembre. Axell explicó que los equipos técnicos y no técnicos serán evaluados, con énfasis en el funcionamiento del artefacto final y la documentación. Se asignaron roles específicos para los equipos, incluyendo a Carolina en el equipo técnico del chatbot, y Axell proporcionó orientación sobre el repositorio y las instrucciones para el desarrollo del proyecto.
