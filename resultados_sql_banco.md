# 🏦 Consultas SQL y Resultados — Riesgo Crediticio y Morosidad

Consultas ejecutadas sobre **`banco_riesgo.db`** (tabla `cartera_creditos`) para evaluar la salud de la cartera y validar el modelo de scoring.

---

### 1. KPIs Generales de la Cartera Crediticia

```sql
SELECT 
    COUNT(ID_Cliente) AS total_clientes,
    ROUND(SUM(Monto_Solicitado), 2) AS cartera_total_usd,
    ROUND(AVG(Monto_Solicitado), 2) AS prestamo_promedio,
    ROUND(AVG(Score_Crediticio), 0) AS score_promedio,
    SUM(Estado_Default) AS clientes_en_default,
    ROUND(AVG(Estado_Default) * 100, 2) AS tasa_morosidad_pct
FROM cartera_creditos;
```

| total_clientes | cartera_total_usd | prestamo_promedio | score_promedio | clientes_en_default | tasa_morosidad_pct |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1,200 | $27,686,427.41 | $23,072.02 | 602 | 136 | **11.33%** |

---

### 2. Morosidad y Capital en Riesgo por Tipo de Préstamo

```sql
SELECT 
    Tipo_Prestamo,
    COUNT(ID_Cliente) AS cantidad_creditos,
    ROUND(SUM(Monto_Solicitado), 2) AS capital_otorgado,
    ROUND(SUM(CASE WHEN Estado_Default = 1 THEN Monto_Solicitado ELSE 0 END), 2) AS capital_en_riesgo,
    ROUND(AVG(Estado_Default) * 100, 2) AS tasa_morosidad_pct
FROM cartera_creditos
GROUP BY Tipo_Prestamo
ORDER BY tasa_morosidad_pct DESC;
```

| Tipo_Prestamo | cantidad_creditos | capital_otorgado | capital_en_riesgo | tasa_morosidad_pct |
| :--- | :---: | :---: | :---: | :---: |
| **Personal** | 462 | $10,671,196.95 | **$1,453,115.49** | **13.62%** |
| **Automotriz** | 253 | $5,801,254.02 | $636,053.18 | 10.97% |
| **PyME** | 142 | $3,275,906.84 | $344,121.05 | 10.51% |
| **Hipotecario** | 343 | $7,938,069.60 | $717,584.12 | 9.04% |

---

### 3. Validación del Scoring Crediticio

```sql
SELECT 
    Segmento_Riesgo,
    COUNT(ID_Cliente) AS clientes,
    ROUND(AVG(Ingreso_Mensual), 2) AS ingreso_promedio,
    ROUND(AVG(Ratio_Deuda_Ingreso), 2) AS ratio_deuda_ingreso_prom,
    ROUND(AVG(Estado_Default) * 100, 2) AS tasa_morosidad_pct
FROM cartera_creditos
GROUP BY Segmento_Riesgo
ORDER BY tasa_morosidad_pct DESC;
```

| Segmento_Riesgo | clientes | ingreso_promedio | ratio_deuda_ingreso_prom | tasa_morosidad_pct |
| :--- | :---: | :---: | :---: | :---: |
| **Alto Riesgo** | 464 | $2,812.40 | 0.89 | **22.63%** |
| **Riesgo Medio** | 369 | $2,845.15 | 0.84 | 6.50% |
| **Bajo Riesgo** | 367 | $2,798.90 | 0.86 | **1.63%** |
