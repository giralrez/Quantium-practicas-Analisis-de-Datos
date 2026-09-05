# Outputs - Informe Quantium Chips

Esta carpeta contiene todos los archivos generados por el informe de análisis de chips.

## Estructura

```
outputs/
├── csv_powerbi/           # CSV listos para importar a Power BI
│   ├── kpis_resumen.csv
│   ├── metricas_mensuales.csv
│   ├── ventas_por_segmento.csv
│   ├── afinidad_marcas.csv
│   ├── afinidad_paquetes.csv
│   ├── evaluacion_trial.csv
│   └── tendencia_mensual.csv
├── visualizaciones/       # Gráficos en alta resolución (PNG)
│   ├── kpi_summary.png
│   ├── heatmap_segmentos.png
│   ├── top_segmentos.png
│   ├── top_marcas.png
│   ├── afinidad_marcas.png
│   ├── distribucion_paquetes.png
│   ├── afinidad_paquetes.png
│   ├── tendencia_ventas.png
│   ├── trial_evaluation.png
│   └── conclusiones.png
└── dashboard/             # Dashboard interactivo
    └── quantium_dashboard.py
```

## Uso

### 1. Para Power BI
1. Abrir Power BI Desktop
2. Seleccionar "Get Data" → "Text/CSV"
3. Importar cada archivo CSV de `csv_powerbi/`
4. Crear visualizaciones usando los campos disponibles

### 2. Para Visualizaciones Estáticas
1. Abrir `notebooks/quantium_insights_report.ipynb` en Jupyter
2. Ejecutar todas las celdas
3. Los PNG se guardarán automáticamente en `visualizaciones/`

### 3. Para Dashboard Interactivo
1. Instalar dependencias: `pip install plotly dash dash-bootstrap-components`
2. Ejecutar: `python dashboard/quantium_dashboard.py`
3. Abrir http://127.0.0.1:8050 en el navegador

## Métricas Incluidas

### KPIs Principales
- Ventas Totales
- Unidades Totales
- Clientes Únicos
- Ticket Promedio
- Precio Promedio por Unidad

### Análisis por Segmento
- LIFESTAGE × PREMIUM_CUSTOMER
- Participación en ventas
- Ticket promedio por segmento

### Análisis de Marcas
- Market share por marca
- Índice de afinidad por segmento

### Tamaño de Paquete
- Distribución de ventas por tamaño
- Índice de afinidad por tamaño

### Evaluación de Trial
- Comparativa tiendas 77, 86, 88 vs control
- Resultados estadísticos (t-values)
- Significancia estadística

## Notas

- Los CSV están en formato UTF-8 con BOM para compatibilidad con Excel
- Los PNG están a 300 DPI para calidad de impresión
- El dashboard es responsive y funciona en móvil
