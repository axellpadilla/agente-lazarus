FROM mcr.microsoft.com/devcontainers/python:3.13

# Instalar uv
# Metodo pip
# RUN pip install --no-cache-dir uv

# Metodo recomendado en docker (https://docs.astral.sh/uv/getting-started/installation/)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copiar archivos de configuración del proyecto
COPY pyproject.toml ./
COPY src/ ./src/

# Crear el entorno virtual y sincronizar dependencias
RUN uv sync

# El modo devcontainer hace el montaje de los archivos y demas configuracion para el devcontainer
