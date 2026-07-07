# 🥔 Análisis de Segmentos de Clientes y Comportamiento de Compra de Chips

Análisis de datos de transacciones y comportamiento de clientes para la categoría de **chips**, desarrollado como base de una recomendación estratégica para la revisión de categoría solicitada por la Gerencia Comercial.

## 📋 Contexto del proyecto

Este proyecto responde a una solicitud de análisis para respaldar con datos una recomendación estratégica sobre la categoría de chips. El objetivo es comprender las tendencias y comportamientos de compra actuales, identificando **quién compra chips**, **cuánto gasta** y **qué unidades consume** según distintos segmentos de clientes, con el fin de traducir estos hallazgos en una estrategia de negocio accionable.

**Pregunta de negocio central:** ¿Qué segmentos de clientes impulsan las ventas de chips y cómo puede la categoría capitalizar ese comportamiento?

## 🎯 Objetivos

- Realizar limpieza y validación de los datos (formatos, valores atípicos, consistencia).
- Enriquecer el dataset con características derivadas (marca, tamaño de paquete, segmento de cliente).
- Definir métricas clave para describir el comportamiento de compra por segmento.
- Generar insights con aplicación comercial directa.
- Traducir los hallazgos en una recomendación estratégica clara y respaldada por datos.

## 🗂️ Estructura del repositorio

```
├── data/
│   ├── raw/                  # Datos originales sin procesar
│   └── processed/            # Datos limpios y enriquecidos
├── notebooks/
│   └── analysis.R            # (o .ipynb) Análisis exploratorio y de segmentación
├── outputs/
│   ├── figures/               # Gráficos y visualizaciones
│   └── findings_report.pdf   # Reporte de hallazgos iniciales
├── README.md
└── requirements.txt / DESCRIPTION
```

## 🔍 Metodología

1. **Chequeo de calidad de datos**
   - Resúmenes estadísticos de alto nivel (summary, glimpse, describe).
   - Detección y tratamiento de valores atípicos.
   - Validación y corrección de formatos (fechas, tipos de dato, unidades).

2. **Ingeniería de características**
   - Extracción de marca y tamaño de paquete a partir del nombre del producto.
   - Clasificación de clientes por segmentos (vida, edad, nivel de ingreso, etc. según dataset).

3. **Definición de métricas**
   - Gasto total y promedio por segmento.
   - Unidades compradas por transacción/segmento.
   - Frecuencia de compra.
   - Marca y tamaño de paquete preferido por segmento.

4. **Análisis y visualización**
   - Comparación de comportamiento entre segmentos.
   - Identificación de segmentos de alto valor y oportunidades de crecimiento.

## 🛠️ Stack técnico

- **R** (dplyr, ggplot2, data.table) — análisis principal
- **Python** (pandas, matplotlib/seaborn) — análisis complementario
- **CSV** como formato de datos fuente

## 📊 Hallazgos iniciales

> *Sección en construcción — se actualizará con los insights obtenidos tras el análisis exploratorio y de segmentación.*

- Segmento(s) con mayor gasto total: _pendiente_
- Segmento(s) con mayor volumen de unidades: _pendiente_
- Marcas y tamaños de paquete preferidos por segmento: _pendiente_

## 💡 Recomendación estratégica preliminar

> *Se documentará una vez consolidados los hallazgos, enfocada en acciones concretas para la revisión de categoría (mix de producto, pricing, promociones dirigidas por segmento).*

## 🚀 Cómo ejecutar el análisis

```bash
# Clonar el repositorio
git clone https://github.com/giralrez/<nombre-del-repo>.git
cd <nombre-del-repo>

# Ejecutar en R
Rscript notebooks/analysis.R
```

## 👤 Autor

**Andrés Giraldo Ramírez (Midas)**
Software Engineer en transición hacia Data Analytics / ML / Data Engineering
GitHub: [@giralrez](https://github.com/giralrez)

---

*Este análisis forma parte de un ejercicio de estudio de caso abierto orientado a la práctica de habilidades de análisis de datos aplicadas a un contexto de negocio real.*
