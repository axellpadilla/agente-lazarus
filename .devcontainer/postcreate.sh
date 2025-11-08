#!/bin/bash
set -e

echo "🚀 Lazarus Dev Container - Configuración Post-Creación"
echo "======================================================"

# Códigos de color
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

# 1. Verificar instalación de Python
echo -e "\n${YELLOW}[1/4]${NC} Verificando instalación de Python 3.13..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION encontrado"

# 2. Verificar uv (ya instalado en la imagen)
echo -e "\n${YELLOW}[2/4]${NC} Verificando uv..."
UV_VERSION=$(uv --version 2>&1 || echo "uv no encontrado")
echo -e "${GREEN}✓${NC} $UV_VERSION"

# 3. Verificar dependencias (ya sincronizadas en la imagen)
echo -e "\n${YELLOW}[3/4]${NC} Verificando dependencias del proyecto..."
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓${NC} Entorno virtual encontrado"
else
    echo -e "${RED}✗${NC} Entorno virtual no encontrado"
    exit 1
fi

# 4. Pruebas rápidas de validación
echo -e "\n${YELLOW}[4/4]${NC} Ejecutando pruebas de validación..."
python -c "
import sys
try:
    import dspy
    import pandas
    import openpyxl
    print('✓ Dependencias principales verificadas')
    sys.exit(0)
except ImportError as e:
    print(f'✗ Error de importación: {e}')
    sys.exit(1)
" || exit 1

echo -e "\n${GREEN}🎉 ¡Configuración completa!${NC}"
echo -e "\nPróximos pasos:"
echo -e "  1. Configurar archivo .env: ${YELLOW}cp .env.example .env${NC}"
echo -e "  2. Agregar tus credenciales LLM (p.ej. LITELLM_API_KEY o LITELLM_API_BASE) en .env"
echo -e "  3. Ejecutar el chatbot: ${YELLOW}python chatbot.py${NC}"
echo -e "  4. O ejecutar ejemplos: ${YELLOW}python ejemplo.py${NC}"
