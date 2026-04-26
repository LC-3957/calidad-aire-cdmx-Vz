import pandas as pd
import numpy as np
import glob
import os


# CONFIGURACIÓN DE RUTAS
RUTA_MEDIAS   = "AIRE_CDMX_2011_2021/AIRE/contaminantes/medias/horarios"
RUTA_CATS     = "AIRE_CDMX_2011_2021/AIRE/catalogos"
RUTA_SALIDA   = "datos_procesados"

PARAMS        = ['NO2', 'O3', 'PM2.5']   # NO2 como proxy de tráfico
AÑOS_VALIDOS  = range(2011, 2022)         # 2011–2021 según el proyecto

DIAS_ORDEN    = ['Lunes', 'Martes', 'Miércoles', 'Jueves',
                 'Viernes', 'Sábado', 'Domingo']
DIAS_MAP      = {0:'Lunes', 1:'Martes', 2:'Miércoles', 3:'Jueves',
                 4:'Viernes', 5:'Sábado', 6:'Domingo'}

os.makedirs(RUTA_SALIDA, exist_ok=True)


# 1. CARGAR CATÁLOGOS

print("Cargando catálogos...")
cat_estaciones = pd.read_csv(f"{RUTA_CATS}/cat_estacion.csv",  encoding='latin-1')
cat_parametros = pd.read_csv(f"{RUTA_CATS}/cat_parametros.csv", encoding='latin-1')
cat_unidades   = pd.read_csv(f"{RUTA_CATS}/cat_unidades.csv",   encoding='latin-1')

print(f"  {len(cat_estaciones)} estaciones  |  {len(cat_parametros)} parámetros")


# 2. CARGAR Y COMBINAR ARCHIVOS CRUDOS

print("\nCargando archivos medias6h...")
archivos = sorted(glob.glob(f"{RUTA_MEDIAS}/medias6h_*.csv"))

fragmentos = []
for archivo in archivos:
    año = int(os.path.basename(archivo).replace("medias6h_", "").replace(".csv", ""))
    if año not in AÑOS_VALIDOS:
        print(f"  [SKIP] {año} fuera del rango 2011-2021")
        continue

    df = pd.read_csv(archivo, encoding='latin-1')

    # Verificar columnas esperadas
    cols_req = {'date', 'id_station', 'id_parameter', 'value'}
    if not cols_req.issubset(df.columns):
        print(f"  [WARN] {año}: columnas inesperadas {df.columns.tolist()}")
        continue

    # Filtrar solo los contaminantes de interés
    df = df[df['id_parameter'].isin(PARAMS)].copy()
    if df.empty:
        print(f"  [WARN] {año}: sin registros para {PARAMS}")
        continue

    df['año'] = año
    fragmentos.append(df)
    print(f"  {año}: {len(df):,} registros cargados")

df_raw = pd.concat(fragmentos, ignore_index=True)
print(f"\nTotal crudo: {len(df_raw):,} registros")


# 3. LIMPIEZA

print("\nLimpiando datos...")

# Parsear fechas
df_raw['date'] = pd.to_datetime(df_raw['date'], errors='coerce')
antes = len(df_raw)
df_raw = df_raw.dropna(subset=['date', 'value'])
print(f"  Eliminados por fecha/valor nulo: {antes - len(df_raw):,}")

# Eliminar valores negativos (errores de sensor)
antes = len(df_raw)
df_raw = df_raw[df_raw['value'] >= 0]
print(f"  Eliminados por valor negativo: {antes - len(df_raw):,}")

# Eliminar outliers extremos por contaminante (percentil 99.5)
print("  Aplicando filtro de outliers (p99.5) por contaminante...")
for param in PARAMS:
    mask  = df_raw['id_parameter'] == param
    p995  = df_raw.loc[mask, 'value'].quantile(0.995)
    antes = mask.sum()
    df_raw = df_raw[~(mask & (df_raw['value'] > p995))]
    print(f"    {param}: límite superior = {p995:.1f}  "
          f"| eliminados = {antes - (df_raw['id_parameter'] == param).sum():,}")

print(f"  Registros limpios totales: {len(df_raw):,}")


# 4. ENRIQUECER CON VARIABLES TEMPORALES

df_raw['dia']      = df_raw['date'].dt.dayofweek.map(DIAS_MAP)
df_raw['hora']     = df_raw['date'].dt.hour
df_raw['mes']      = df_raw['date'].dt.month
df_raw['es_finde'] = df_raw['dia'].isin(['Sábado', 'Domingo'])


# 5. COBERTURA — documentar para la presentación

print("\nCobertura por año y contaminante:")
cob = (df_raw.groupby(['año', 'id_parameter'])['value']
       .count()
       .unstack(fill_value=0))
print(cob.to_string())
cob.to_csv(f"{RUTA_SALIDA}/cobertura_por_año.csv")


# 6. DATASET VIZ 1 — Heatmap hora × día  (proxy de tráfico: NO2)

print("\nGenerando dataset Viz 1 (heatmap NO2)...")

viz1 = (df_raw[df_raw['id_parameter'] == 'NO2']
        .groupby(['dia', 'hora'])['value']
        .mean()
        .reset_index()
        .rename(columns={'value': 'NO2_ppb'}))

viz1['dia'] = pd.Categorical(viz1['dia'], categories=DIAS_ORDEN, ordered=True)
viz1 = viz1.sort_values(['dia', 'hora']).reset_index(drop=True)
viz1['NO2_ppb'] = viz1['NO2_ppb'].round(2)

viz1.to_csv(f"{RUTA_SALIDA}/viz1_heatmap_no2.csv", index=False)
print(f"  {len(viz1)} filas guardadas → viz1_heatmap_no2.csv")


# 7. DATASET VIZ 2 — Líneas NO2 vs O3 (normalizadas 0-100)

print("\nGenerando dataset Viz 2 (líneas NO2 vs O3)...")

viz2_no2 = (df_raw[df_raw['id_parameter'] == 'NO2']
            .groupby(['dia', 'hora'])['value']
            .mean()
            .reset_index()
            .rename(columns={'value': 'NO2_ppb'}))

viz2_o3  = (df_raw[df_raw['id_parameter'] == 'O3']
            .groupby(['dia', 'hora'])['value']
            .mean()
            .reset_index()
            .rename(columns={'value': 'O3_ppb'}))

viz2 = viz2_no2.merge(viz2_o3, on=['dia', 'hora'])

# Normalización 0-100 para que público general pueda comparar
def normalizar(serie):
    mn, mx = serie.min(), serie.max()
    return ((serie - mn) / (mx - mn) * 100).round(1)

viz2['NO2_norm'] = normalizar(viz2['NO2_ppb'])
viz2['O3_norm']  = normalizar(viz2['O3_ppb'])

viz2['dia'] = pd.Categorical(viz2['dia'], categories=DIAS_ORDEN, ordered=True)
viz2 = viz2.sort_values(['dia', 'hora']).reset_index(drop=True)

viz2.to_csv(f"{RUTA_SALIDA}/viz2_lineas_no2_o3.csv", index=False)
print(f"  {len(viz2)} filas guardadas → viz2_lineas_no2_o3.csv")

# 8. DATASET VIZ 3 — Ranking de días por O3 (peor para salud)

print("\nGenerando dataset Viz 3 (ranking días por O3)...")

viz3 = (df_raw[df_raw['id_parameter'] == 'O3']
        .groupby('dia')['value']
        .agg(
            O3_promedio='mean',
            O3_p75=lambda x: x.quantile(0.75),   # horas que son malas frecuentes
            O3_p90=lambda x: x.quantile(0.90),   # horas que son muy malas
            n_registros='count'
        )
        .reset_index()
        .rename(columns={'value': 'O3_ppb'}))

viz3['dia'] = pd.Categorical(viz3['dia'], categories=DIAS_ORDEN, ordered=True)
viz3 = viz3.sort_values('O3_promedio', ascending=False).reset_index(drop=True)
viz3['rank'] = viz3.index + 1

for col in ['O3_promedio', 'O3_p75', 'O3_p90']:
    viz3[col] = viz3[col].round(2)

viz3.to_csv(f"{RUTA_SALIDA}/viz3_ranking_dias_o3.csv", index=False)
print(f"  {len(viz3)} filas guardadas → viz3_ranking_dias_o3.csv")
print(viz3[['rank', 'dia', 'O3_promedio']].to_string(index=False))


df_raw.to_csv(f"{RUTA_SALIDA}/datos_completos_limpios.csv", index=False)
print(f"\nDatos completos guardados → datos_completos_limpios.csv")
print("\nProcesamiento finalizado.")