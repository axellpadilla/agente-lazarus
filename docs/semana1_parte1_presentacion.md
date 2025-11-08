🧱 **Temática Clave — Gobernanza y Diagnóstico de Datos

- **Fundamento para modelos predictivos:** Establecer una base de calidad y gobernanza de datos para asegurar que los modelos (por ejemplo, regresión) usen información confiable y consistente.
- **Conceptos clave:** Ciclo de vida del dato, propiedad del dato (Data Ownership), frecuencia de actualización y calidad de los datos.
- **Diagnóstico de procesos actuales:** Discusión sobre adquisición de datos de inventario y demanda (grado de manualidad, orígenes, responsables, inconsistencias históricas).
- **Políticas y datos maestros:** Definición práctica de propiedad y reglas de calidad para el chatbot y los datos maestros de producto (reemplazos, equivalencias, descontinuados).
- **Transición a automatización:** Necesidad de mover fuentes dispersas (CSV/Excel) a fuentes centralizadas (DB / APIs) para mejorar frescura y consistencia.

## ✅ Conclusiones y Tareas Inmediatas

- **Estructura de Gobernanza:** Se inició el borrador del documento de Políticas de Datos (objetivos, propiedad, frecuencia, reglas de calidad — p. ej. tratamiento de valores negativos en ventas).
- **Práctica hands-on:** Comentarios y colaboración en Google Docs sobre la política de calidad de datos.
  - Documento: https://docs.google.com/document/d/1fs_5OlaqA9bSvlnAiqphmMjU0WoyXRFi58mg5u-dFKM/edit?usp=sharing
  - Responsables: (spreadsheet): https://docs.google.com/spreadsheets/d/14Z234SdSEWD3fBGmCkWVkYiJxaIvdUWdpw82KJd0bXc/edit?usp=sharing
- **Consolidación de responsabilidades:** Asignación de dueños para la gestión de datos clave.

- **Asignación (tarea):** Completar el borrador de Reglas de Calidad y avanzar con el documento de Gobernanza de Datos para el chatbot de atención al cliente.

## Contenido y Exactitud

Se enfoca en garantizar que la información sea correcta, verificable y no contenga contradicciones internas. Puntos clave:

- Definir fuentes primarias de verdad (single source of truth) para cada tipo de contenido.
- Establecer procesos de validación y revisión antes de publicar en la base del chatbot.

## Cobertura y Utilidad

Se enfoca en que el chatbot responda a las preguntas esperadas y que las respuestas sean útiles:

- Mapear preguntas frecuentes y casos de uso prioritarios.
- Medir cobertura periódicamente (porcentaje de preguntas atendidas correctamente) y cerrar brechas.

## Estructura y Formato

Se centra en cómo almacenar y organizar los datos para el motor del chatbot:

- Estandarizar formatos (fechas ISO 8601, códigos de producto, campos obligatorios).
- Usar metadatos (fuente, versión, fecha_actualizacion, nivel_confianza) para cada registro.

## Mantenimiento y Ciclo de Vida

Se centra en responsabilidades y en mantener contenido vigente:

- Definir cadencias de revisión (diaria/ semanal/ mensual) según criticidad de la fuente.
- Registrar responsable, fecha de última revisión y próximo vencimiento en cada dataset.

## Fuentes de Datos del Chatbot

| Fuente de Datos | Dueño interno |
|-----------------|---------------|
| Preguntas frecuentes de clientes | (Análisis de Datos) |
| Guías de usuario técnicas (proveedores) | Mercadeo |
| Guías de usuario promocionales | Mercadeo |
| Base de datos de productos (incluye imágenes) | Mercadeo / Análisis de Datos / Abastecimiento |

## Fuentes de Datos de Análisis de Compra

| Fuente de Datos | Dueño interno |
|-----------------|---------------|
| Base de datos de productos (incluye imágenes) | Mercadeo / Análisis de Datos / Abastecimiento |
| Datos maestros de planificación | (Abastecimiento) / Comercial |

## Tabla ejemplo: Datos Maestros (importante)

| id_producto | id_producto_equivalente | factor_numerador | factor_denominador | tipo_registro | fecha_desde | fecha_hasta | notas |
|-------------:|:------------------------:|------------------:|-------------------:|:--------------:|:-----------:|:-----------:|:-----|
| PROD-000123 | PROD-000045 | 100 | 1 | activo | 2024-01-01 | 2099-12-31 | Producto con factor de conversión 100:1 |

Notas:

- `fecha_desde` y `fecha_hasta` en formato `YYYY-MM-DD` (ISO 8601).
- `tipo_registro`: ejemplo `activo`, `descontinuado`, `equivalente`.
- `factor_numerador` / `factor_denominador`: usar enteros, no decimales; documentar la unidad de conversión en `notas`.

