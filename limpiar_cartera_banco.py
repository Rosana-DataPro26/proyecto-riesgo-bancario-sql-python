import pandas as pd
import numpy as np
import sqlite3

# 1. Cargar dataset crudo
df = pd.read_csv('cartera_creditos_sucia.csv')
print(f"Filas iniciales: {len(df)}")

# 2. Eliminar registros duplicados por ID_Cliente
df = df.drop_duplicates(subset=['ID_Cliente']).copy()

# 3. Estandarizar categorías de Tipo_Prestamo (quitar espacios y unificar mayúsculas)
df['Tipo_Prestamo'] = df['Tipo_Prestamo'].str.strip().str.capitalize()
df['Tipo_Prestamo'] = df['Tipo_Prestamo'].replace({'Pyme': 'PyME'})

# 4. Limpiar Ingreso_Mensual (convertir negativos en nulos e imputar con la mediana)
df.loc[df['Ingreso_Mensual'] <= 0, 'Ingreso_Mensual'] = np.nan
mediana_ingreso = df['Ingreso_Mensual'].median()
df['Ingreso_Mensual'] = df['Ingreso_Mensual'].fillna(mediana_ingreso).round(2)

# 5. Limpiar Score_Crediticio (rango válido bancario: 300 a 850)
df.loc[(df['Score_Crediticio'] < 300) | (df['Score_Crediticio'] > 850), 'Score_Crediticio'] = np.nan
mediana_score = int(df['Score_Crediticio'].median())
df['Score_Crediticio'] = df['Score_Crediticio'].fillna(mediana_score).astype(int)

# 6. Ingeniería de variables (KPIs individuales de riesgo)
df['Ratio_Deuda_Ingreso'] = np.round(df['Monto_Solicitado'] / (df['Ingreso_Mensual'] * 12), 2)

condiciones = [
    (df['Score_Crediticio'] >= 700),
    (df['Score_Crediticio'] >= 550) & (df['Score_Crediticio'] < 700),
    (df['Score_Crediticio'] < 550)
]
categorias = ['Bajo Riesgo', 'Riesgo Medio', 'Alto Riesgo']
df['Segmento_Riesgo'] = np.select(condiciones, categorias, default='Riesgo Medio')

# 7. Exportar a Excel limpio y guardar en Base de Datos SQLite
df.to_excel('cartera_creditos_limpia.xlsx', index=False)

conexion = sqlite3.connect('banco_riesgo.db')
df.to_sql('cartera_creditos', conexion, if_exists='replace', index=False)
conexion.close()

print(f"Limpieza completada: {len(df)} clientes únicos guardados en 'banco_riesgo.db' (tabla: cartera_creditos)")
print("\nDistribución por Segmento de Riesgo:")
print(df['Segmento_Riesgo'].value_counts())