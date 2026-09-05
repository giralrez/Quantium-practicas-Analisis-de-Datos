# Análisis de Categoría Chips - Quantium

Análisis de datos de transacciones y comportamiento de clientes para la categoría de **chips**, desarrollado como base de una recomendación estratégica para la revisión de categoría solicitada por la Gerencia Comercial.

## Contexto del proyecto

Este proyecto responde a una solicitud de análisis para respaldar con datos una recomendación estratégica sobre la categoría de chips. El objetivo es comprender las tendencias y comportamientos de compra actuales, identificando **quién compra chips**, **cuánto gasta** y **qué unidades consume** según distintos segmentos de clientes.

**Pregunta de negocio central:** ¿Qué segmentos de clientes impulsan las ventas de chips y cómo puede la categoría capitalizar ese comportamiento?

## Estructura del proyecto

```
├── data/
│   ├── raw/                        # Datos originales sin procesar
│   └── processed/                  # Datos limpios y enriquecidos
├── notebooks/
│   ├── analysis.R                  # (o .ipynb) Análisis exploratorio y de segmentación
│   └── quantium_insights_report.ipynb  # Genera las 10 visualizaciones PNG
├── scripts/
│   └── powerbi_export.py           # Genera los 7 CSV para Power BI
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
│   ├── visualizaciones/            # PNG generados por el notebook de insights
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
│   └── findings_report.pdf         # Reporte de hallazgos iniciales
├── README.md
└── requirements.txt / DESCRIPTION
```

## Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

- **R** (dplyr, ggplot2, data.table) — análisis principal
- **Python** (pandas, matplotlib/seaborn) — análisis complementario
- **Plotly Dash** — dashboard interactivo para exploración de resultados
- **CSV** como formato de datos fuente

## 📊 Visualizaciones

10 gráficos generados con `notebooks/quantium_insights_report.ipynb`, disponibles en [`outputs/visualizaciones/`](./outputs/visualizaciones).

### KPIs y conclusiones ejecutivas

| KPI Summary | Conclusiones |
|---|---|
| ![KPI Summary](./outputs/visualizaciones/kpi_summary.png) | ![Conclusiones](./outputs/visualizaciones/conclusiones.png) |

### Segmentos de clientes

| Top segmentos | Heatmap de segmentos |
|---|---|
| ![Top segmentos](./outputs/visualizaciones/top_segmentos.png) | ![Heatmap segmentos](./outputs/visualizaciones/heatmap_segmentos.png) |

### Marcas y paquetes

| Top marcas | Afinidad por marcas |
|---|---|
| ![Top marcas](./outputs/visualizaciones/top_marcas.png) | ![Afinidad marcas](./outputs/visualizaciones/afinidad_marcas.png) |

| Distribución de paquetes | Afinidad por paquetes |
|---|---|
| ![Distribución paquetes](./outputs/visualizaciones/distribucion_paquetes.png) | ![Afinidad paquetes](./outputs/visualizaciones/afinidad_paquetes.png) |

### Tendencia y evaluación de trial

| Tendencia de ventas | Evaluación trial vs. control |
|---|---|
| ![Tendencia de ventas](./outputs/visualizaciones/tendencia_ventas.png) | ![Evaluación trial](./outputs/visualizaciones/trial_evaluation.png) |

## 📈 Dashboard interactivo (Plotly Dash)

Además de las visualizaciones estáticas, el proyecto incluye un dashboard interactivo construido con **Plotly Dash** que permite explorar los resultados de forma dinámica: filtrar por segmento, marca y tamaño de paquete, y comparar métricas clave (gasto, unidades, frecuencia de compra) sin necesidad de regenerar gráficos manualmente.

**Funcionalidades principales:**
- Filtros interactivos por segmento de cliente, marca y tamaño de paquete.
- KPIs dinámicos que se actualizan según la selección.
- Gráficos de tendencia, distribución y afinidad equivalentes a los de `outputs/visualizaciones/`, pero explorables en tiempo real.

> Instrucciones de ejecución en el [Paso 4](#-cómo-ejecutar-el-proyecto) más abajo.

## 📑 Contenido del informe

| Componente | Métricas / Insights |
|---|---|
| **KPIs** | Ventas, unidades, clientes, ticket promedio, precio/unidad |
| **Segmentos** | 12 segmentos LIFESTAGE × PREMIUM, con ventas, clientes y frecuencia |
| **Marcas** | Top 10 marcas, market share, índice de afinidad |
| **Paquetes** | Distribución por tamaño, afinidad por segmento |
| **Tendencia** | Evolución mensual de ventas, unidades y clientes |
| **Trial** | Evaluación tiendas 77, 86, 88 vs. control (233, 155, 237) |

## 📊 Hallazgos iniciales

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

## 🚀 Cómo ejecutar el proyecto

### Tamaño de Paquete
- Distribución de ventas por tamaño
- Índice de afinidad por tamaño

# Instalar dependencias
pip install -r requirements.txt
```

**Paso 1: Análisis exploratorio y de segmentación**

```bash
Rscript notebooks/analysis.R
```

**Paso 2: Exportar datos para Power BI**

```bash
python scripts/powerbi_export.py
```

Genera 7 CSV en `outputs/csv_powerbi/`:
- `kpis_resumen.csv` — KPIs globales
- `metricas_mensuales.csv` — Métricas por tienda/mes
- `ventas_por_segmento.csv` — LIFESTAGE × PREMIUM
- `afinidad_marcas.csv` — Índice de afinidad por marca
- `afinidad_paquetes.csv` — Índice de afinidad por tamaño
- `tendencia_mensual.csv` — Serie temporal
- `evaluacion_trial.csv` — Resultados estadísticos

**Paso 3: Generar visualizaciones PNG**

```bash
jupyter notebook notebooks/quantium_insights_report.ipynb
```

Ejecutar todas las celdas para generar 10 PNG en `outputs/visualizaciones/`:
- `kpi_summary.png` — Cards con KPIs
- `heatmap_segmentos.png` — Heatmap de ventas
- `top_segmentos.png` — Top 10 segmentos
- `top_marcas.png` — Market share
- `afinidad_marcas.png` — Índice de afinidad
- `distribucion_paquetes.png` — Ventas por tamaño
- `afinidad_paquetes.png` — Afinidad por tamaño
- `tendencia_ventas.png` — Evolución mensual
- `trial_evaluation.png` — Comparativa trial vs. control
- `conclusiones.png` — Tabla ejecutiva

**Paso 4: Dashboard interactivo**

```bash
python dashboard/quantium_dashboard.py
```

Acceder a [`http://127.0.0.1:8050`](http://127.0.0.1:8050).

## 👤 Autor

**Andrés Gidaldo Ramírez**
Software Engineer | Data Analytics / ML / Data Engineering
GitHub: [@giralrez](https://github.com/giralrez)

---

*Este análisis forma parte de un ejercicio de estudio de caso del Quantium Virtual Internship.*
