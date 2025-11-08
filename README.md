# Agente Lazarus - Chatbot Inteligente con RAG

Bot conversacional inteligente que utiliza RAG (Retrieval-Augmented Generation) para responder preguntas basadas en una base de conocimientos en formato CSV. Implementado con Python 3.13, DSPy y proveedores de IA compatibles con DSPy.

## 🚀 Características

- **Python 3.13** con devcontainer configurado
- **RAG (Retrieval-Augmented Generation)** con un retriever DSPy que consume la base de conocimientos limpia (`data_limpia/faq_limpio.csv`)
- **DSPy** para orquestación de prompts y cadenas de razonamiento estructuradas
- **Proveedores de IA compatibles con DSPy** (OpenAI, Anthropic, etc.) para acceso a modelos de IA
- **Transferencia inteligente a agente humano** guiada por un módulo DSPy de decisión
- **Modo interactivo** de chat y script de regresiones rápidas (`ejemplo.py`)

## 📋 Requisitos

- Python 3.13+
- API key de un proveedor compatible con DSPy (opcional para funcionalidad completa)

## 🛠️ Instalación

### Opción 1: Usando devcontainer (Recomendado)

1. Abrir el repositorio en VS Code
2. Cuando se solicite, seleccionar "Reopen in Container"
3. El contenedor ejecutará automáticamente el script `postcreate.sh` que:
   - Verifica Python 3.13
   - Instala `uv` (gestor de paquetes de Astral)
   - Descarga todas las dependencias
   - Valida archivos críticos
   - Ejecuta smoke tests

### Opción 2: Instalación local

```bash
# 1. Instalar uv (si no lo tienes)
pip install uv

# 2. Sincronizar dependencias con uv
cd /workspaces/agente-lazarous
uv sync

# 3. Copiar archivo de configuración
cp .env.example .env

# 4. Editar .env y agregar tu API key
# DSPY_API_KEY=tu_api_key_aqui
# DSPY_MODEL=openai/gpt-3.5-turbo (o el modelo de tu proveedor)
```

**Nota:** El proyecto usa `uv` workspace con dos paquetes locales. El comando `uv sync` instala todo (incluyendo paquetes locales editables) en un único `.venv` compartido.

## 📖 Uso

**Nota:** Todos los comandos de ejecución deben precederse con `uv run` para asegurar que se use el entorno virtual correcto del workspace. Ejemplo: `uv run python -m lazarus_apps.main`

### 1. Chatbot Interactivo

```bash
uv run python -m lazarus_apps.main
```

Esto iniciará una sesión de chat interactiva donde puedes hacer preguntas sobre Grupo Lazarus.

### 2. UI Streamlit

```bash
uv run streamlit run src/lazarus_apps/ui.py
```

Interfaz web interactiva con:
- Historial de chat
- Estadísticas de base de conocimientos
- Expandibles con detalles de respuesta
- Información sobre transferencias

### 4. Tareas de VS Code

El proyecto incluye tareas preconfiguradas en `.vscode/tasks.json` para facilitar el uso:

- **uv-run**: Ejecuta `uv run` con argumentos personalizados (ej: `python ejemplo.py`)
- **uv-sync**: Ejecuta `uv sync` con argumentos opcionales (ej: `--upgrade`)

Para usarlas: `Ctrl+Shift+P` > "Tasks: Run Task" > Seleccionar tarea > Ingresar argumentos cuando se solicite.

### 4. Workshop ETL Semana 1 (Parte 2)

La carpeta `docs/` contiene el guion completo de la sesión y el cuaderno `notebooks/demo_etl.ipynb` implementa la demo paso a paso:

1. Abre el repositorio en Codespaces (o en tu entorno local con VS Code).
2. Verifica que el archivo bruto `faq_grupo_lazarus.xlsx` esté disponible en la raíz del proyecto.
3. Ejecuta el notebook `notebooks/demo_etl.ipynb` siguiendo las celdas en orden para cubrir el flujo **Extract → Transform → Load**.
4. Durante la demo, apóyate en `docs/semana1_parte2_presentacion.md` para los tiempos, discursos sugeridos y momentos clave.
5. Al finalizar, muestra el archivo `data_limpia/faq_limpio.csv` generado para cerrar el ciclo ETL.

### 5. Uso Programático

```python
from lazarus_core import LazarusChatbot
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancia del chatbot
chatbot = LazarusChatbot()

# Hacer una pregunta
response = chatbot.answer("¿Cuál es el horario de atención?")
print(response['answer'])
```

## 🗂️ Estructura del Proyecto (Workspace uv)

```
agente-lazarous/
├── pyproject.toml                  # ROOT workspace (define members)
├── uv.lock                         # Lockfile compartido
│
├── packages/                       # Miembros del workspace
│   ├── lazarus-core/              # Backend: chatbot con DSPy
│   │   ├── src/lazarus_core/
│   │   │   ├── __init__.py
│   │   │   ├── bot.py             # LazarusChatbot (DSPy Module)
│   │   │   ├── retriever.py       # FAQRetriever
│   │   │   ├── signatures.py      # DSPy signatures
│   │   │   ├── structures.py      # ChatResult dataclass
│   │   │   ├── constants.py       # Constantes
│   │   │   └── main.py            # Entry point CLI
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   └── lazarus-kb/                # Knowledge base: FAQ
│       ├── src/lazarus_kb/
│       │   ├── __init__.py
│       │   └── knowledge_base.py  # FAQKnowledgeBase (búsqueda)
│       ├── pyproject.toml
│       └── README.md
│
├── src/lazarus_apps/               # Aplicación raíz (UI + CLI)
│   ├── __init__.py
│   ├── main.py                     # CLI interactivo
│   ├── ui.py                       # UI Streamlit (NUEVA)
│   └── ...
│
├── scripts/                        # Scripts utilitarios
│   └── etl_malo.py                # ETL: Excel → CSV
│
├── data_limpia/                    # Datos FAQ procesados
│   └── faq_limpio.csv
│
├── .devcontainer/                 # Devcontainer config
├── docs/                          # Documentación
├── notebooks/                     # Notebooks (demo ETL)
├── data/                          # Datos originales (Excel)
├── ejemplo.py                     # Ejemplos de uso
└── README.md                      # Este archivo
```

**Arquitectura:**
- **lazarus-kb**: Gestiona búsqueda en FAQ (importable por otros proyectos)
- **lazarus-core**: Orquesta DSPy + retriever (depende de lazarus-kb)
- **lazarus-apps**: CLI e interfaz Streamlit (depende de lazarus-core)
- **Un único .venv**: Todos los paquetes en modo editable compartido

## 🔧 Configuración

### Variables de Entorno

Crear un archivo `.env` con las siguientes variables:

```bash
# API Key del proveedor de IA (obligatorio)
DSPY_API_KEY=tu_api_key_aqui

# Modelo a utilizar en formato DSPy: provider/model-name (obligatorio)
# Ejemplos:
#   openai/gpt-3.5-turbo
#   anthropic/claude-3-haiku-20240307
#   cohere/command
#   openrouter/openai/gpt-3.5-turbo
DSPY_MODEL=openai/gpt-3.5-turbo

# Opcional: URL base personalizada (para gateways, proxies, etc.)
# DSPY_API_BASE=https://tu-gateway-endpoint/v1
```

### Obtener API Key

El proceso depende de tu proveedor:

**OpenAI:**
1. Visitar [https://platform.openai.com](https://platform.openai.com)
2. Crear una cuenta
3. Ir a API Keys → Create new secret key
4. Copiar la key a `DSPY_API_KEY`

**Anthropic (Claude):**
1. Visitar [https://console.anthropic.com](https://console.anthropic.com)
2. Crear una cuenta
3. Ir a API Keys
4. Copiar la key a `DSPY_API_KEY` y usa `DSPY_MODEL=anthropic/claude-3-haiku-20240307`

**Otros proveedores:**
Consulta la [documentación de DSPy LM](https://dspy.ai/api/models/LM/) para configuración específica.

## 📊 Base de Conocimientos

El archivo `faq_grupo_lazarus.xlsx` contiene la base de conocimientos con las siguientes columnas:

- **Pregunta**: La pregunta frecuente
- **Respuesta**: La respuesta correspondiente
- **Categoría**: Categoría de la pregunta (Horarios, Soporte, Servicios, etc.)

El archivo se procesa a través del notebook `notebooks/demo_etl.ipynb` para generar `data_limpia/faq_limpio.csv` que es consumido por `lazarus-kb`.

### Actualizar la Base de Conocimientos

Para agregar nuevas preguntas y respuestas:

1. Abrir `faq_grupo_lazarus.xlsx` en Excel
2. Agregar nuevas filas con Pregunta, Respuesta y Categoría
3. Guardar el archivo
4. Ejecutar el ETL desde `notebooks/demo_etl.ipynb`
5. El CSV actualizado se generará en `data_limpia/faq_limpio.csv`
6. Reiniciar el chatbot para cargar los nuevos datos

## 🤖 Funcionamiento del RAG + DSPy

1. **Recuperación** (`lazarus_kb.FAQKnowledgeBase.search()`): busca en el CSV con matching de palabras clave y manejo de sinónimos.

2. **Adaptación DSPy** (`lazarus_core.retriever.FAQRetriever`): adapta el retriever a `dspy.Module` para entregar pasajes y metadatos.

3. **Generación estructurada** (`lazarus_core.signatures.CustomerServiceSignature` con `dspy.ChainOfThought`): produce saludo, respuesta directa y próxima acción usando el contexto recuperado.

4. **Transferencia inteligente** (`lazarus_core.signatures.TransferDecisionSignature`): decide si escalar a agente humano considerando la respuesta generada.

5. **Fallback**: Sin API key se responde con la FAQ literal, manteniendo el mismo contrato `ChatResult` (backward compatible).

## 🎯 Ejemplos de Preguntas

Preguntas que el chatbot puede responder:

- ¿Cuál es el horario de atención?
- ¿Cómo contacto a soporte técnico?
- ¿Qué servicios ofrecen?
- ¿Dónde están ubicadas las oficinas?
- ¿Aceptan pagos con tarjeta?
- ¿Cuál es el tiempo de entrega?
- ¿Tienen garantía?

## 🔄 Transferencia a Agente

Cuando el chatbot no encuentra información relevante en la base de conocimientos:

1. Informa al usuario que no tiene la información
2. Simula una transferencia a un agente humano
3. Muestra información sobre el proceso de transferencia
4. Registra la pregunta para futura referencia

## 🚀 Modelos Disponibles

DSPy soporta múltiples proveedores. El usuario especifica el modelo en formato `gateway/provider/model-name`:

- **OpenAI**: `openai/gpt-3.5-turbo`, `openai/gpt-4`, `openai/gpt-4-turbo`
- **Anthropic**: `anthropic/claude-3-haiku-20240307`, `anthropic/claude-3-sonnet-20240229`
- **Cohere**: `cohere/command`
- **OpenRouter**: `openrouter/openai/gpt-3.5-turbo`, `openrouter/anthropic/claude-2`, etc.
- **Otros**: Consulta [documentación de DSPy LM](https://dspy.ai/api/models/LM/)

Para usar un proveedor específico, establece `DSPY_MODEL` con el formato adecuado y `DSPY_API_KEY` con tu credencial.

## 🐛 Solución de Problemas

### El devcontainer falla al crearse

- El script `postcreate.sh` verifica automáticamente:
  - Python 3.13 disponible
  - `uv` instalado correctamente
  - Todas las dependencias descargadas
  - Archivos críticos presentes
- Si hay error, verifica los logs del devcontainer en la pestaña de "Dev Container" en VS Code

### El chatbot no puede acceder a la API

- Verificar que `DSPY_API_KEY` y `DSPY_MODEL` estén configuradas en `.env`
- Verificar que la API key sea válida para el proveedor especificado
- Si usas un gateway personalizado, asegúrate de que `DSPY_API_BASE` sea correcto
- El chatbot funcionará en modo fallback sin API key (respuestas directas sin DSPy)

### No se encuentra el archivo Excel

- Verificar que `faq_grupo_lazarus.xlsx` esté en el directorio raíz
- El script postcreate advierte si falta este archivo
- Verificar permisos de lectura del archivo

### Error al sincronizar dependencias

```bash
# Con uv (recomendado)
uv sync --upgrade

# O si hay problemas, resetear el lock
rm uv.lock
uv sync
```

### Error de importación en código

Si ves errores como `ModuleNotFoundError: No module named 'chatbot_demo'`:
- Asegúrate de estar usando imports nuevos: `from lazarus_core import LazarusChatbot`
- Ejecuta `uv sync` nuevamente para actualizar paquetes editables
- Reinicia el terminal o el IDE para actualizar la ruta de módulos

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📧 Contacto

Para preguntas o soporte, contactar a soporte@grupolazarus.com
