🧩 **Temática Clave — Algoritmos de ML, Optimización y Pipelines de Datos**

- **Fundamentos de Modelado:** Diferenciación entre modelos lineales (regresión) y no lineales (árboles), y su aplicación según la naturaleza de los datos.
- **Estrategia de Pronóstico (MVP):** Adopción de un enfoque de "fuerza bruta" basado en reglas simples (longitud de serie, coeficiente de variación) antes de aplicar modelos complejos.
- **Reestructuración del Pipeline:** División del flujo de trabajo en preprocesamiento seguro, entrenamiento y clasificación para mejorar la modularidad y seguridad.
- **Resolución de Dependencias Técnicas:** Solución a conflictos en Jupyter Notebooks mediante la selección correcta de Kernels (Punto B) y sincronización de entornos (V Sync).
- **Métricas de Evaluación:** Uso del Error Cuadrático Medio (MSE) y R-cuadrado ($R^2$) como estándares para comparar el desempeño entre modelos y promedios simples.

## ✅ Conclusiones y Tareas Inmediatas

- **División de Equipos de Trabajo:**
  - **Equipo Benchmarking:** (Luis Sabillon, Nelson, Carolina) Investigar y comparar herramientas/estándares externos.
  - **Equipo Técnico:** (Luis Castillo, Franklin, Evelyn) Corregir errores de código, tipos de datos (fechas) y nomenclatura de variables.
- **Definición del MVP:** Filtrar productos utilizando reglas de negocio básicas (volumen de ventas, coeficiente de variación) para decidir qué productos requieren modelos avanzados y cuáles se gestionan por promedios.
- **Estandarización Técnica:** Axell compartió el enlace actualizado del repositorio y guio la configuración del espacio de trabajo para asegurar que todos usen el mismo Kernel.
- **Medición de Errores:** Compromiso de registrar y comparar los errores de los modelos versus los valores reales para validar la efectividad del pronóstico.

## 🧠 Contenido Principal de la Sesión

### Modelos de Machine Learning y Clasificación
- Se explicaron las diferencias críticas entre **regresión** (predicción de valores continuos numéricos) y **clasificación** (predicción de etiquetas/categorías).
- Se discutió el uso de:
  - **Regresión Lineal y Logística:** Para relaciones directas y clasificaciones binarias.
  - **Árboles de Decisión:** Para capturar relaciones no lineales en los datos.
- **Criterio de Selección:** El modelo con el menor Error Cuadrático Medio (MSE) será seleccionado automáticamente para cada producto.

### Estrategia de "Fuerza Bruta" y Reglas de Negocio
- Se determinó que no todos los productos requieren modelos complejos ("matar moscas a cañonazos").
- **Métricas de decisión:**
  - **Longitud de la serie:** Se requiere un mínimo de 3 puntos de datos para regresiones lineales.
  - **Coeficiente de Variación (CV):** Si la variabilidad es baja, un promedio simple puede ser superior a un modelo complejo.
- **Workflow:** Filtrar datos $\rightarrow$ Evaluar reglas simples $\rightarrow$ Aplicar ML solo donde aporte valor $\rightarrow$ Comparar contra realidad.

### Ingeniería de Pipelines y Modularidad
- Hubo un cambio estructural en el pipeline de seguridad:
  1. **Preprocesamiento seguro:** Limpieza y transformación.
  2. **Entrenamiento:** Separación de Regresión y Clasificación.
- Se demostró cómo las funciones de limpieza y carga se han encapsulado en paquetes reutilizables, permitiendo importarlas en distintos notebooks sin reescribir código.

### Diagnóstico Técnico y Entorno (Jupyter/Kernels)
- Se abordaron los bloqueos técnicos recurrentes (errores de librerías e importación).
- **Solución implementada:**
  - Cambio al Kernel específico "Punto B" donde residen las librerías correctas.
  - Uso de **uv sync** para asegurar la instalación de todas las dependencias en el entorno local.
- Se enfatizó que las librerías instaladas son persistentes en el Kernel seleccionado, facilitando la reutilización entre proyectos.

### Data Splitting y Data Leakage
- Se reforzó la práctica obligatoria de separar los datos en **Entrenamiento** (Training) y **Prueba** (Test) antes de entrenar.
- En la evaluación preliminar, se observó que modelos como *Tree Progress* mostraban errores más uniformes y menor sesgo en los datos de prueba en comparación con modelos lineales simples para ciertos productos.

## 🛠️ Herramientas Utilizadas y Recursos

| Herramienta | Descripción | Uso en la sesión |
|:---|:---|:---|
| **Jupyter Notebook** | Entorno interactivo de desarrollo. | Ejecución de pipelines de ML y visualización de errores. |
| **uv sync** | Herramienta de sincronización. | Instalación y homologación de dependencias del equipo. |
| **Scikit-Learn** | Librería de ML para Python. | Implementación de regresiones, árboles y métricas (MSE). |
| **GitHub** | Repositorio de código. | Control de versiones y distribución del código corregido. |

## 📌 Próximos Pasos

1. **Todos:** Filtrar productos para el MVP usando las reglas de Coeficiente de Variación y Longitud de Serie.
2. **Todos:** Ejecutar los modelos, medir el error vs. realidad y guardar el modelo ganador para cada producto.
3. **Luis C. / Franklin / Evelyn:** Reparar tipos de datos (fechas) y nombres de variables en el código base.
4. **Próxima Sesión:** Se abordará a profundidad la optimización de hiperparámetros para refinar los modelos seleccionados.