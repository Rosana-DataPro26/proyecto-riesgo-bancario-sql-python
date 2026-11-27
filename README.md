# 🏦 Análisis de Riesgo Crediticio y Morosidad Bancaria (ETL + SQL + Power BI)

## 📌 Resumen del Proyecto
Proyecto integral de análisis de datos aplicado al **Sector Bancario**, orientado a auditar una cartera de **1.200 créditos**, limpiar anomalías de origen, validar el modelo de scoring crediticio y detectar exposición al incumplimiento (*default*).

## 🛠️ Stack Tecnológico y Flujo de Trabajo
1. **Python (`pandas`, `numpy`, `sqlite3`):** Auditoría de calidad de datos (`limpiar_cartera_banco.py`), eliminación de duplicados, imputación por mediana de ingresos nulos/negativos, corrección de outliers en *Score Crediticio* (rango 300–850) y cálculo del *Ratio Deuda/Ingreso*.
2. **SQLite (`banco_riesgo.db`):** Almacenamiento relacional y ejecución de consultas analíticas de negocio.
3. **Power BI + DAX (`dashboard_bancario.pbix.pbix`):** Modelado de medidas ejecutivas y tablero interactivo para el Comité de Riesgos.

## 📊 Dashboard Ejecutivo
![Dashboard Riesgo Bancario](./Proyecto%20Bancario.png)

## 💡 Hallazgos Clave del Negocio
* **Salud Global de Cartera:** Volumen total de **$27,69 millones** con una tasa de morosidad del **11,33%** (136 clientes en default) y score crediticio promedio de **602 puntos**.
* **Exposición por Línea de Crédito:** Los préstamos **Personales** presentan la mayor morosidad (**13,62%**, con $1,45M en riesgo), mientras que los **Hipotecarios** son los más resilientes (**9,04%**).
* **Efectividad del Scoring:** El segmento de **Alto Riesgo** concentra una tasa de default del **22,63%**, frente a apenas el **1,63%** en **Bajo Riesgo**, validando la segmentación preventiva.

## 📂 Exploración de Código y Resultados
* **Consultas y Tablas SQL:** Revisá las queries completas junto con sus resultados en [`resultados_sql_banco.md`](./resultados_sql_banco.md).
