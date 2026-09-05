#!/bin/bash
# Script de ejecución rápida para el informe Quantium
# Ejecuta todos los componentes del informe

echo "=========================================="
echo "  INFORME QUANTIUM - CHIPS ANALYSIS"
echo "=========================================="
echo ""

# Verificar si Python está disponible
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no encontrado"
    exit 1
fi

# Verificar dependencias
echo "Verificando dependencias..."
python3 -c "import pandas, numpy, matplotlib, seaborn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependencias básicas..."
    pip3 install pandas numpy matplotlib seaborn scipy openpyxl
fi

python3 -c "import plotly, dash" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependencias adicionales..."
    pip3 install plotly dash dash-bootstrap-components kaleido
fi

echo ""
echo "Paso 1: Exportando datos para Power BI..."
python3 scripts/powerbi_export.py
echo ""

echo "Paso 2: Generando visualizaciones (ejecutar notebook)..."
echo "  Abre notebooks/quantium_insights_report.ipynb en Jupyter"
echo "  y ejecuta todas las celdas para generar los PNG"
echo ""

echo "Paso 3: Iniciando dashboard interactivo..."
echo "  Para ejecutar: python3 dashboard/quantium_dashboard.py"
echo "  Accede a http://127.0.0.1:8050"
echo ""

echo "=========================================="
echo "  ARCHIVOS GENERADOS:"
echo "=========================================="
echo ""
echo "CSV para Power BI:"
ls -la outputs/csv_powerbi/*.csv 2>/dev/null || echo "  (Ejecutar powerbi_export.py primero)"
echo ""
echo "Visualizaciones PNG:"
ls -la outputs/visualizaciones/*.png 2>/dev/null || echo "  (Ejecutar notebook primero)"
echo ""
echo "Dashboard:"
ls -la dashboard/*.py 2>/dev/null
echo ""
echo "=========================================="
echo "  ¡Listo!"
echo "=========================================="
