import pandas as pd
import os

RUTA_DATOS = os.path.join(os.path.dirname(__file__), "..", "datos_procesados")

DIAS_ORDEN = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']


def _normalizar_columnas(df):
    """Renombra 'dia' → 'Dia' y 'hora' → 'hora' para consistencia."""
    renombrar = {}
    for col in df.columns:
        if col.lower() == 'dia':
            renombrar[col] = 'Dia'
        if col.lower() == 'hora':
            renombrar[col] = 'hora'
    return df.rename(columns=renombrar)


def _aplicar_orden_dias(df, col='Dia'):
    df[col] = pd.Categorical(df[col], categories=DIAS_ORDEN, ordered=True)
    return df


def cargar_viz1_barras():
    ruta = os.path.join("datos_procesados", "viz1_barras_no2.csv")
    df = pd.read_csv(ruta)
    df = _normalizar_columnas(df)
    df = _aplicar_orden_dias(df)
    df = df.sort_values(['Dia', 'hora'])
    return df


def cargar_viz2_lineas():
    ruta = os.path.join("datos_procesados", "viz2_lineas_no2_o3.csv")
    df = pd.read_csv(ruta)
    df = _normalizar_columnas(df)
    df = _aplicar_orden_dias(df)

    df_diario = (
        df.groupby('Dia', observed=True)[['NO2_norm', 'O3_norm', 'NO2_ppb', 'O3_ppb']]
        .mean()
        .reset_index()
    )
    df_diario = df_diario.sort_values('Dia')
    for col in ['NO2_norm', 'O3_norm', 'NO2_ppb', 'O3_ppb']:
        df_diario[col] = df_diario[col].round(1)
    return df_diario


def cargar_viz3_ranking():
    ruta = os.path.join("datos_procesados", "viz3_ranking_dias_o3.csv")
    df = pd.read_csv(ruta)
    df = _normalizar_columnas(df)
    df = _aplicar_orden_dias(df)
    df = df.sort_values('O3_promedio', ascending=True)
    return df


def cargar_barras_pivot():
    df = cargar_viz1_barras()
    pivot = df.pivot_table(index='hora', columns='Dia', values='NO2_ppb', observed=True)
    pivot = pivot.reindex(columns=DIAS_ORDEN)
    return pivot