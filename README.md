# Agente Lazarus - Chatbot Inteligente con RAG

Bot conversacional inteligente que utiliza RAG (Retrieval-Augmented Generation) para responder preguntas basadas en una base de conocimientos en formato Excel. Implementado con Python 3.13, DSPy y OpenRouter API.

## 🚀 Características

- **Python 3.13** con devcontainer configurado
- **RAG (Retrieval-Augmented Generation)** para búsqueda en base de conocimientos
- **DSPy** para orquestación de prompts y respuestas
- **OpenRouter API** para acceso a múltiples modelos de IA (GPT-3.5, GPT-4, Claude, etc.)
- **Base de conocimientos Excel** (faq_grupo_lazarus.xlsx)
- **Transferencia inteligente a agente humano** cuando no encuentra respuestas
- **Modo interactivo** de chat

## 📋 Requisitos

- Python 3.13+
- OpenRouter API key (opcional para funcionalidad completa)

## 🛠️ Instalación

### Opción 1: Usando devcontainer (Recomendado)

1. Abrir el repositorio en VS Code
2. Cuando se solicite, seleccionar "Reopen in Container"
3. El contenedor instalará automáticamente todas las dependencias

### Opción 2: Instalación local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Editar .env y agregar tu API key de OpenRouter
# OPENROUTER_API_KEY=tu_api_key_aqui
```

## 📖 Uso

### 1. Chatbot Interactivo

```bash
python chatbot.py
```

Esto iniciará una sesión de chat interactiva donde puedes hacer preguntas sobre Grupo Lazarus.

### 2. Ejemplos de Uso

```bash
python ejemplo.py
```

Este script ejecuta varios ejemplos que demuestran:
- Consultas básicas a la base de conocimientos
- Escenarios de transferencia a agente humano
- Inspección de la base de conocimientos
- Uso con diferentes modelos de IA

### 3. Uso Programático

```python
from chatbot import LazarusChatbot
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancia del chatbot
chatbot = LazarusChatbot()

# Hacer una pregunta
response = chatbot.answer("¿Cuál es el horario de atención?")
print(response['answer'])
```

## 🗂️ Estructura del Proyecto

```
.
├── .devcontainer/
│   └── devcontainer.json          # Configuración del devcontainer
├── chatbot.py                      # Chatbot principal con DSPy
├── rag_knowledge_base.py           # Sistema RAG para búsqueda en Excel
├── ejemplo.py                      # Ejemplos de uso
├── faq_grupo_lazarus.xlsx          # Base de conocimientos (FAQ)
├── requirements.txt                # Dependencias Python
├── .env.example                    # Plantilla de configuración
├── .gitignore                      # Archivos ignorados por git
└── README.md                       # Este archivo
```

## 🔧 Configuración

### Variables de Entorno

Crear un archivo `.env` con las siguientes variables:

```bash
# API Key de OpenRouter (obligatorio para funcionalidad completa)
OPENROUTER_API_KEY=tu_api_key_aqui

# Modelo a utilizar (opcional, default: openai/gpt-3.5-turbo)
MODEL=openai/gpt-3.5-turbo
```

### Obtener API Key de OpenRouter

1. Visitar [https://openrouter.ai](https://openrouter.ai)
2. Crear una cuenta
3. Ir a [https://openrouter.ai/keys](https://openrouter.ai/keys)
4. Generar una nueva API key
5. Copiar la key al archivo `.env`

## 📊 Base de Conocimientos

El archivo `faq_grupo_lazarus.xlsx` contiene la base de conocimientos con las siguientes columnas:

- **Pregunta**: La pregunta frecuente
- **Respuesta**: La respuesta correspondiente
- **Categoría**: Categoría de la pregunta (Horarios, Soporte, Servicios, etc.)

### Actualizar la Base de Conocimientos

Para agregar nuevas preguntas y respuestas:

1. Abrir `faq_grupo_lazarus.xlsx` en Excel
2. Agregar nuevas filas con Pregunta, Respuesta y Categoría
3. Guardar el archivo
4. Reiniciar el chatbot

## 🤖 Funcionamiento del RAG

1. **Búsqueda**: El usuario hace una pregunta
2. **Recuperación**: El sistema busca en la base de conocimientos FAQs relacionadas
3. **Generación**: Si encuentra información relevante, DSPy genera una respuesta contextual
4. **Transferencia**: Si no encuentra información, simula una transferencia a agente humano

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

OpenRouter soporta múltiples modelos:

- `openai/gpt-3.5-turbo` (Rápido y económico)
- `openai/gpt-4` (Más preciso)
- `anthropic/claude-2` (Excelente para conversaciones)
- `google/palm-2-chat-bison` (Alternativa de Google)
- Y muchos más...

## 🐛 Solución de Problemas

### El chatbot no puede acceder a la API

- Verificar que `OPENROUTER_API_KEY` esté configurada en `.env`
- Verificar que la API key sea válida
- El chatbot funcionará en modo fallback sin API key (respuestas directas sin DSPy)

### No se encuentra el archivo Excel

- Verificar que `faq_grupo_lazarus.xlsx` esté en el directorio raíz
- Verificar permisos de lectura del archivo

### Error al instalar dependencias

```bash
# Actualizar pip primero
pip install --upgrade pip

# Instalar dependencias una por una si hay conflictos
pip install dspy-ai
pip install pandas openpyxl
```

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
