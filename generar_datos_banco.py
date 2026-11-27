import pandas as pd
import numpy as np

np.random.seed(42)
n = 1200

datos = {
    'ID_Cliente': [f'CLI-{1000+i}' for i in range(n)],
    'Edad': np.random.randint(21, 72, size=n),
    'Ingreso_Mensual': np.round(np.random.normal(2800, 1100, size=n), 2),
    'Antiguedad_Laboral_Anios': np.random.randint(0, 30, size=n),
    'Score_Crediticio': np.random.randint(350, 850, size=n),
    'Tipo_Prestamo': np.random.choice(['Personal', 'Hipotecario', 'Automotriz', 'PyME', 'personal ', 'HIPOTECARIO'], size=n, p=[0.35, 0.25, 0.20, 0.12, 0.04, 0.04]),
    'Monto_Solicitado': np.round(np.random.uniform(1500, 45000, size=n), 2),
    'Plazo_Meses': np.random.choice([12, 24, 36, 48, 60], size=n),
    'Cuotas_Atrasadas': np.random.choice([0, 0, 0, 1, 2, 3, 5, 8], size=n, p=[0.55, 0.10, 0.05, 0.10, 0.08, 0.06, 0.04, 0.02]),
    'Region': np.random.choice(['AMBA', 'Centro', 'Cuyo', 'Norte', 'Patagonia'], size=n)
}

df = pd.DataFrame(datos)

# Ajuste realista: a menor score y mayor atraso, mayor probabilidad de Default (1 = Moroso grave, 0 = Al día)
prob_default = (
    (850 - df['Score_Crediticio']) / 1000 +
    (df['Cuotas_Atrasadas'] * 0.08) +
    np.where(df['Ingreso_Mensual'] < 1800, 0.15, 0)
)
df['Estado_Default'] = np.where(prob_default > 0.58, 1, 0)

# Introducimos "suciedad" realista para limpiar en el Paso 2:
df.loc[np.random.choice(df.index, 25), 'Ingreso_Mensual'] = np.nan          # Nulos en ingresos
df.loc[np.random.choice(df.index, 12), 'Ingreso_Mensual'] = -500.00         # Ingresos negativos imposibles
df.loc[np.random.choice(df.index, 15), 'Score_Crediticio'] = 9999           # Outliers de score fuera de rango (300-850)
df = pd.concat([df, df.iloc[:18]], ignore_index=True)                       # 18 registros duplicados

df.to_csv('cartera_creditos_sucia.csv', index=False, encoding='utf-8')
print(f"Archivo generado con éxito: {len(df)} filas guardadas en cartera_creditos_sucia.csv")