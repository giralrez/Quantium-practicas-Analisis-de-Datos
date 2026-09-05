# Análisis de Categoría Chips - Quantium

Análisis de datos de transacciones y comportamiento de clientes para la categoría de **chips**, desarrollado como base de una recomendación estratégica para la revisión de categoría solicitada por la Gerencia Comercial.

## Contexto del proyecto

Este proyecto responde a una solicitud de análisis para respaldar con datos una recomendación estratégica sobre la categoría de chips. El objetivo es comprender las tendencias y comportamientos de compra actuales, identificando **quién compra chips**, **cuánto gasta** y **qué unidades consume** según distintos segmentos de clientes.

**Pregunta de negocio central:** ¿Qué segmentos de clientes impulsan las ventas de chips y cómo puede la categoría capitalizar ese comportamiento?

## Estructura del proyecto

```
├── data/
│   ├── raw/                        # Datos originales sin procesar
│   │   ├── QVI_data.csv
│   │   ├── QVI_data_2.csv
│   │   ├── QVI_purchase_behaviour.csv
│   │   └── QVI_transaction_data.xlsx
│   └── processed/                  # Datos limpios y enriquecidos
├── notebooks/
│   ├── Quantium_Task1_EDA_Python.ipynb   # Análisis exploratorio y limpieza
│   ├── Task2_Quantium_Python.ipynb        # Evaluación de tiendas trial
│   └── quantium_insights_report.ipynb     # Genera 10 visualizaciones PNG
├── scripts/
│   └── powerbi_export.py           # Genera 7 CSV para Power BI
├── dashboard/
│   └── quantium_dashboard.py       # Dashboard interactivo (Plotly Dash)
├── outputs/
│   ├── csv_powerbi/                # CSV exportados para Power BI
│   │   ├── kpis_resumen.csv
│   │   ├── metricas_mensuales.csv
│   │   ├── ventas_por_segmento.csv
│   │   ├── afinidad_marcas.csv
│   │   ├── afinidad_paquetes.csv
│   │   ├── tendencia_mensual.csv
│   │   └── evaluacion_trial.csv
│   ├── visualizaciones/            # PNG generados por el notebook
│   │   ├── kpi_summary.png
│   │   ├── heatmap_segmentos.png
│   │   ├── top_segmentos.png
│   │   ├── top_marcas.png
│   │   ├── afinidad_marcas.png
│   │   ├── distribucion_paquetes.png
│   │   ├── afinidad_paquetes.png
│   │   ├── tendencia_ventas.png
│   │   ├── trial_evaluation.png
│   │   └── conclusiones.png
│   ├── findings_report.pdf         # Reporte de hallazgos
│   └── README.md                   # Documentación de outputs
├── docs/                           # Documentación de referencia
│   ├── InsideSherpa_Task1_DraftSolutions - Template.pdf
│   ├── InsideSherpa_Task2_DraftSolutions - Template.pdf
│   ├── Quantium_Task1_EDA_Python.html
│   ├── Quantium_Task1_EDA_Python.pdf
│   ├── Task2_Quantium_Python.html
│   ├── Task2_Quantium_Python.pdf
│   ├── Quantium Virtual Internship - Task 1.pdf
│   └── Quantium Virtual Internship - Task 2.pdf
├── requirements.txt
├── run_report.sh
└── README.md
```

## Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Exportar datos para Power BI
```bash
python scripts/powerbi_export.py
```

### 3. Generar visualizaciones PNG
```bash
jupyter notebook notebooks/quantium_insights_report.ipynb
```
Ejecutar todas las celdas para generar los 10 PNG en `outputs/visualizaciones/`.

### 4. Dashboard interactivo
```bash
python dashboard/quantium_dashboard.py
```
Acceder a http://127.0.0.1:8050

## Métricas del informe

### KPIs Principales
- Ventas Totales
- Unidades Totales
- Clientes Únicos
- Ticket Promedio
- Precio Promedio por Unidad

### Análisis por Segmento
- 12 segmentos LIFESTAGE × PREMIUM_CUSTOMER
- Participación en ventas por segmento
- Ticket promedio por segmento

### Análisis de Marcas
- Top 10 marcas por market share
- Índice de afinidad por segmento

### Tamaño de Paquete
- Distribución de ventas por tamaño
- Índice de afinidad por tamaño

### Evaluación de Trial
- Comparativa tiendas 77, 86, 88 vs control
- Resultados estadísticos (t-values)
- Significancia estadística (|t| > 1.895)

## Autor

**Andrés Gidaldo Ramírez**
Software Engineer | Data Analytics / ML / Data Engineering
GitHub: [@giralrez](https://github.com/giralrez)

---

*Este análisis forma parte de un ejercicio de estudio de caso del Quantium Virtual Internship.*
