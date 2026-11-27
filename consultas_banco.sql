-- ============================================================================
-- PROYECTO 2: Análisis de Riesgo Crediticio y Morosidad Bancaria
-- BASE DE DATOS: banco_riesgo.db (SQLite) | TABLA: cartera_creditos
-- ============================================================================

-- 1. KPIs GENERALES DE LA CARTERA CREDITICIA
-- Mide el volumen total prestado, ticket promedio y tasa global de morosidad (Default).
SELECT 
    COUNT(ID_Cliente) AS total_clientes,
    ROUND(SUM(Monto_Solicitado), 2) AS cartera_total_usd,
    ROUND(AVG(Monto_Solicitado), 2) AS prestamo_promedio,
    ROUND(AVG(Score_Crediticio), 0) AS score_promedio,
    SUM(Estado_Default) AS clientes_en_default,
    ROUND(AVG(Estado_Default) * 100, 2) AS tasa_morosidad_pct
FROM cartera_creditos;


-- 2. TASA DE MOROSIDAD Y EXPOSICIÓN POR TIPO DE PRÉSTAMO
-- Identifica qué línea de crédito concentra mayor capital en riesgo.
SELECT 
    Tipo_Prestamo,
    COUNT(ID_Cliente) AS cantidad_creditos,
    ROUND(SUM(Monto_Solicitado), 2) AS capital_otorgado,
    ROUND(SUM(CASE WHEN Estado_Default = 1 THEN Monto_Solicitado ELSE 0 END), 2) AS capital_en_riesgo,
    ROUND(AVG(Estado_Default) * 100, 2) AS tasa_morosidad_pct
FROM cartera_creditos
GROUP BY Tipo_Prestamo
ORDER BY tasa_morosidad_pct DESC;


-- 3. VALIDACIÓN DEL MODELO DE SCORING (SEGMENTO DE RIESGO VS. DEFAULT REAL)
-- Comprueba si los clientes clasificados como "Alto Riesgo" efectivamente caen más en mora.
SELECT 
    Segmento_Riesgo,
    COUNT(ID_Cliente) AS clientes,
    ROUND(AVG(Ingreso_Mensual), 2) AS ingreso_promedio,
    ROUND(AVG(Ratio_Deuda_Ingreso), 2) AS ratio_deuda_ingreso_prom,
    ROUND(AVG(Estado_Default) * 100, 2) AS tasa_morosidad_pct
FROM cartera_creditos
GROUP BY Segmento_Riesgo
ORDER BY tasa_morosidad_pct DESC;


-- 4. DESEMPEÑO DE CARTERA POR REGIÓN GEOGRÁFICA
-- Detecta zonas con mayor nivel de atraso y morosidad.
SELECT 
    Region,
    COUNT(ID_Cliente) AS total_clientes,
    ROUND(SUM(Monto_Solicitado), 2) AS cartera_regional,
    ROUND(AVG(Cuotas_Atrasadas), 2) AS promedio_cuotas_atrasadas,
    ROUND(AVG(Estado_Default) * 100, 2) AS tasa_morosidad_pct
FROM cartera_creditos
GROUP BY Region
ORDER BY tasa_morosidad_pct DESC;


-- 5. ALERTA TEMPRANA: CLIENTES CRÍTICOS DE ALTO VALOR (CTE + FILTRO DE RIESGO)
-- Detecta los 10 préstamos más altos que aún no están en default pero ya tienen 3 o más cuotas atrasadas.
WITH alerta_preventiva AS (
    SELECT 
        ID_Cliente,
        Tipo_Prestamo,
        Region,
        Score_Crediticio,
        Monto_Solicitado,
        Cuotas_Atrasadas,
        Ratio_Deuda_Ingreso
    FROM cartera_creditos
    WHERE Estado_Default = 0 AND Cuotas_Atrasadas >= 3
)
SELECT *
FROM alerta_preventiva
ORDER BY Monto_Solicitado DESC
LIMIT 10;