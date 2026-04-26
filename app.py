import os
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from data_loader import (
    cargar_viz1_barras,
    cargar_viz2_lineas,
    cargar_viz3_ranking,
    cargar_barras_pivot,
)

# ── Datos ──────────────────────────────────────────────────────────────────
print("Cargando datos...")
df_barras = cargar_viz1_barras()
df_lineas  = cargar_viz2_lineas()
df_ranking = cargar_viz3_ranking()
df_pivot   = cargar_barras_pivot()

# Precarga PM2.5 para que el selector no se trabe
print("Precargando PM2.5...")
_ruta_completo = os.path.join("datos_procesados", "datos_completos_limpios.csv")
df_pm25_precargado = pd.read_csv(_ruta_completo, usecols=['date', 'id_parameter', 'value'])
df_pm25_precargado = df_pm25_precargado[df_pm25_precargado['id_parameter'] == 'PM2.5'].copy()
df_pm25_precargado['date'] = pd.to_datetime(df_pm25_precargado['date'], errors='coerce')
_DIAS_MAP = {0:'Lunes',1:'Martes',2:'Miércoles',3:'Jueves',4:'Viernes',5:'Sábado',6:'Domingo'}
df_pm25_precargado['Dia'] = df_pm25_precargado['date'].dt.dayofweek.map(_DIAS_MAP)
df_pm25_precargado = df_pm25_precargado.dropna(subset=['Dia', 'value'])
print("Datos listos.")

RUTA = os.path.join(os.path.dirname(__file__), "..", "datos_procesados")
DIAS_ORDEN = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

# ── Paleta VERDE ────────────────────────────────────
# Colores principales
C_NO2   = '#2c6e9e'      # Azul verdoso (NO2)
C_O3    = '#d4a017'      # Mostaza/ámbar (Ozono)
C_PM25  = '#c05a3b'      # Terracota (PM2.5)
C_ALERT = '#c05a3b'

# Colores de fondo para gráficas 
C_BG    = '#fefef7'      # Fondo de la gráfica 
C_PAPER = '#fefef7'      # Fondo del papel 
C_GRID  = '#c8e0d0'      # Líneas de cuadrícula 
C_TEXT  = '#1a2e24'      # Texto principal 
C_MUTED = '#4a6b5d'      # Texto secundario 
FONT_BODY = 'Source Sans 3, sans-serif'

# Configuración base de Plotly
PLOTLY_BASE = dict(
    paper_bgcolor=C_PAPER,
    plot_bgcolor=C_BG,
    font=dict(family=FONT_BODY, color=C_TEXT, size=13),
    margin=dict(l=48, r=24, t=48, b=48),
    hoverlabel=dict(
        bgcolor='#e8f4ea',
        bordercolor='#c8e0d0',
        font_color=C_TEXT,
        font_size=13,
    ),
)

# Colores para las barras por hora (Viz 1)
COLORES_HORA = {
    '🌅 6:00 am — Mañana':      '#2c6e9e',   # Azul verdoso
    '☀️ 12:00 pm — Mediodía':   '#d4a017',   # Mostaza
    '🌙 6:00 pm — Tarde-noche': '#c05a3b',   # Terracota
}

# ── App ────────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    assets_folder=os.path.join(os.path.dirname(__file__), "assets")
)
app.title = "¿Respiramos peor los lunes? | Calidad del aire CDMX"
server = app.server

# ── Layout ─────────────────────────────────────────────────────────────────
app.layout = html.Div(className='pagina', children=[

    # HERO
    html.Header(className='hero', children=[
        html.P("Periodismo de datos · CDMX 2011–2021 · SEDEMA / SIMAT",
               className='hero-kicker'),
        html.H1(["¿Respiramos peor ", html.Em("los lunes"), "?"],
                className='hero-titulo'),
        html.P(
            "El tráfico sube de lunes a viernes. Pero el aire más dañino llega después. "
            "Los datos de 10 años de monitoreo en la Ciudad de México cuentan "
            "una historia contraintuitiva sobre contaminación, tráfico y salud.",
            className='hero-subtitulo'
        ),
        html.Div(className='hero-meta', children=[
            html.Div([html.Span("Fuente: "), "SEDEMA · Datos Abiertos CDMX"],
                     className='hero-meta-item'),
            html.Div([html.Span("Período: "), "2011 – 2021"],
                     className='hero-meta-item'),
            html.Div([html.Span("Registros: "), "~3.5 millones"],
                     className='hero-meta-item'),
        ]),
    ]),

    # INTRODUCCIÓN
    html.Section(className='intro-narrativa', children=[
        html.Div(className='intro-texto', children=[
            html.P(
                "¿Has escuchado que los lunes el aire está más contaminado? "
                "Tiene sentido: es el día que más autos salen a la calle "
                "después del fin de semana."
            ),
            html.P([
                html.Strong("Pero los datos cuentan una historia diferente — y un poco inquietante: "),
                "el día de más tráfico NO es el mismo día que más aire dañino respiramos.",
            ]),
            html.P(
                "El NO₂ sale del escape en tiempo real y sigue el ritmo laboral. "
                "El Ozono, es el contaminante que irrita garganta y ojos, se forma "
                "cuando el sol acumula horas sobre esas emisiones. "
                "El daño llega con retraso — incluso hasta el fin de semana."
            ),
        ]),
        html.Div(className='intro-hallazgo', children=[
            html.P("El hallazgo principal", className='intro-hallazgo-label'),
            html.P(
                '"Hay más tráfico entre semana. '
                'Pero el aire más dañino llega el domingo, '
                'cuando nadie lo espera."'
            ),
        ]),
    ]),

    # VIZ 1 — BARRAS TRAFICO
    html.Section(className='seccion-viz', children=[
        html.P("Visualización 01 / 03", className='seccion-numero'),
        html.H2("¿Cuándo hay más autos en la ciudad?", className='seccion-titulo'),
        html.P(
            "El NO₂ (dióxido de nitrógeno) sale directamente del escape de los autos. "
            "Cada grupo de barras muestra tres momentos del día. "
            "Más alta la barra = más NO₂ = más vehículos circulando.",
            className='seccion-descripcion'
        ),
        html.Div(className='grafica-contenedor', children=[
            dcc.Graph(id='barras-trafico', config={'displayModeBar': False}),
        ]),
        html.Div(className='insight', children=[
            html.Strong("Lo que muestran los datos: "),
            "La barra azul (6am) es consistentemente la más alta de lunes a viernes, "
            "con el pico máximo entre martes y jueves. "
            "El domingo es el día más limpio en todos los horarios — "
            "menos autos, menos emisiones directas.",
        ]),
    ]),

    # VIZ 2 — LINEAS
    html.Section(className='seccion-viz', children=[
        html.P("Visualización 02 / 03", className='seccion-numero'),
        html.H2("Si hay más NO₂ entre semana, ¿cuándo sube el Ozono?",
                className='seccion-titulo'),
        html.P(
            "Ambas líneas están en escala 0–100 donde 100 es el peor momento "
            "de la semana para cada contaminante. "
            "Observa que el NO₂ alcanza su pico el viernes, "
            "mientras que el Ozono sube el domingo.",
            className='seccion-descripcion'
        ),
        html.Div(className='leyenda', children=[
            html.Div(className='leyenda-item', children=[
                html.Div(className='leyenda-linea', style={'background': C_NO2}),
                "NO₂ — sale del escape (tráfico en tiempo real)",
            ]),
            html.Div(className='leyenda-item', children=[
                html.Div(className='leyenda-linea', style={
                    'background': 'transparent',
                    'borderTop': f'3px dashed {C_O3}',
                    'height': '0',
                    'marginTop': '6px',
                }),
                "Ozono — se forma con el sol (daño retrasado)",
            ]),
        ]),
        html.Div(className='grafica-contenedor', children=[
            dcc.Graph(id='lineas-no2-o3', config={'displayModeBar': False}),
        ]),
        html.Div(className='insight', children=[
            html.Strong("Lo que muestran los datos: "),
            "El NO₂ sube gradualmente de lunes a viernes y cae el fin de semana — "
            "siguiendo exactamente el patrón del tráfico laboral. "
            "El Ozono, en cambio, es más estable entre semana y tiene su pico el domingo, "
            "cuando el sol acumula horas sobre las emisiones de días anteriores.",
        ]),
    ]),

    # VIZ 3 — RANKING INTERACTIVO
    html.Section(className='seccion-viz', children=[
        html.P("Visualización 03 / 03", className='seccion-numero'),
        html.H2("El ranking: ¿qué día tiene más contaminación?",
                className='seccion-titulo'),
        html.P(
            "Selecciona el contaminante para ver cómo cambia el ranking. "
            "Cada contaminante tiene su propio patrón semanal — "
            "y no todos apuntan al mismo día como el peor.",
            className='seccion-descripcion'
        ),
        html.Div(className='selector-contenedor', children=[
            html.P("Elige el contaminante:", className='selector-label'),
            dcc.RadioItems(
                id='selector-contaminante',
                options=[
                    {'label': ' 🟠 Ozono — daño respiratorio (se forma con el sol)', 'value': 'O3'},
                    {'label': ' 🔵 NO₂ — emisiones de tráfico (sale del escape)', 'value': 'NO2'},
                    {'label': ' 🔴 PM2.5 — partículas finas (entran a los pulmones)', 'value': 'PM25'},
                ],
                value='O3',
                labelStyle={'display': 'block', 'margin': '8px 0', 'color': '#4a6b5d'},
                inputStyle={'marginRight': '10px', 'accentColor': '#2c6e9e'},
            ),
        ]),
        html.Div(className='grafica-contenedor', children=[
            dcc.Graph(id='ranking-dias', config={'displayModeBar': False}),
        ]),
        html.Div(className='insight', children=[
            html.Strong("Lo que revelan los datos: "),
            "Para el Ozono, el domingo es el día más alto — no el lunes ni el jueves. "
            "Las emisiones acumuladas de la semana, procesadas por el sol del fin de semana, "
            "producen su mayor concentración cuando menos lo esperamos. "
            "El mito del 'lunes sucio' apunta al síntoma equivocado.",
        ]),
    ]),

    # CONCLUSION
    html.Section(className='conclusion', children=[
        html.H2("¿Qué hacer con esta información?", className='conclusion-titulo'),
        html.Div(className='conclusion-grid', children=[
            html.Div(className='conclusion-item trafico', children=[
                html.P("De lunes a viernes", className='conclusion-item-titulo'),
                html.P(
                    "El NO₂ sube con el tráfico laboral y alcanza su pico el viernes. "
                    "Son los días de más emisiones directas desde los escapes."
                ),
            ]),
            html.Div(className='conclusion-item ozono', children=[
                html.P("El fin de semana", className='conclusion-item-titulo'),
                html.P(
                    "El Ozono alcanza su concentración más alta el domingo. "
                    "Las emisiones de la semana se transforman con el sol "
                    "y el daño respiratorio llega cuando ya no lo esperamos."
                ),
            ]),
        ]),
        html.Div(className='conclusion-recomendacion', children=[
            html.Strong("Recomendación práctica: "),
            "Si puedes elegir cuándo salir a caminar o hacer ejercicio al aire libre, "
            "considera que ",
            html.Strong("el domingo por la tarde puede tener más Ozono de lo que imaginas"),
            " — especialmente tras una semana de tráfico intenso. "
            "El NO₂ baja el fin de semana, pero el Ozono que irrita garganta y ojos "
            "llega con retraso. Los datos desmienten el mito: "
            "no es el lunes el día más contaminado — es el domingo.",
        ]),
    ]),

    # FOOTER
    html.Footer(className='footer', children=[
        html.P("Fuente: SEDEMA · Sistema de Monitoreo Atmosférico (SIMAT) · "
               "datos.cdmx.gob.mx · Descarga: enero 2025"),
        html.P("Proyecto Final · Visualización Gráfica para IA · "
               "Universidad Iberoamericana León"),
    ]),
])

# ── Callbacks ──────────────────────────────────────────────────────────────

@app.callback(
    Output('barras-trafico', 'figure'),
    Input('barras-trafico', 'id'),
)
def render_barras_trafico(_):
    HORAS_PICO = {
        6:  '🌅 6:00 am — Mañana',
        12: '☀️ 12:00 pm — Mediodía',
        18: '🌙 6:00 pm — Tarde-noche',
    }

    df_plot = df_barras[df_barras['hora'].isin(HORAS_PICO.keys())].copy()
    df_plot['Hora_label'] = df_plot['hora'].map(HORAS_PICO)
    df_agr = df_plot.groupby(['Dia', 'Hora_label'], observed=True)['NO2_ppb'].mean().reset_index()

    fig = go.Figure()
    for hora_label, color in COLORES_HORA.items():
        subset = df_agr[df_agr['Hora_label'] == hora_label]
        fig.add_trace(go.Bar(
            x=subset['Dia'].astype(str),
            y=subset['NO2_ppb'],
            name=hora_label,
            marker_color=color,
            marker_line_width=0,
            opacity=0.9 if "6:00 am" in hora_label else 0.6,
            hovertemplate=(
                "<b>%{x}</b> · " + hora_label.split('—')[1].strip() +
                "<br>NO₂: <b>%{y:.1f} ppb</b>"
                "<br><i>más alto = más autos</i><extra></extra>"
            ),
        ))

    layout = {**PLOTLY_BASE, **dict(
        height=440,
        barmode='group',
        bargap=0.18,
        bargroupgap=0.06,
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.05,
            xanchor='left', x=0,
            font=dict(color=C_MUTED, size=11),
            bgcolor='rgba(0,0,0,0)',
            entrywidth=180,
            entrywidthmode='pixels',
        ),
        xaxis=dict(
            gridcolor=C_GRID,
            tickfont=dict(color=C_TEXT, size=13),
            categoryorder='array',
            categoryarray=DIAS_ORDEN,
            title='',
        ),
        yaxis=dict(
            gridcolor=C_GRID,
            tickfont=dict(color=C_MUTED),
            title='NO₂ (ppb) — más alto = más autos en la calle',
            rangemode='tozero',
        ),
        margin=dict(l=48, r=24, t=80, b=48),
    )}
    fig.update_layout(**layout)
    return fig


@app.callback(
    Output('lineas-no2-o3', 'figure'),
    Input('lineas-no2-o3', 'id'),
)
def render_lineas(_):
    df = df_lineas.copy()
    dias_str = df['Dia'].astype(str).tolist()

    fig = go.Figure()

    # Líneas base
    fig.add_trace(go.Scatter(
        x=dias_str, y=df['NO2_norm'],
        mode='lines+markers',
        line=dict(color=C_NO2, width=3),
        marker=dict(size=8),
        name='NO₂',
    ))

    fig.add_trace(go.Scatter(
        x=dias_str, y=df['O3_norm'],
        mode='lines+markers',
        line=dict(color=C_O3, width=3, dash='dash'),
        marker=dict(size=8, symbol='diamond'),
        name='Ozono',
    ))

    #  Detectar picos automáticamente
    idx_no2 = df['NO2_norm'].idxmax()
    idx_o3 = df['O3_norm'].idxmax()

    dia_no2 = df.loc[idx_no2, 'Dia']
    val_no2 = df.loc[idx_no2, 'NO2_norm']

    dia_o3 = df.loc[idx_o3, 'Dia']
    val_o3 = df.loc[idx_o3, 'O3_norm']

    #  Highlight NO2
    fig.add_trace(go.Scatter(
        x=[str(dia_no2)],
        y=[val_no2],
        mode='markers',
        marker=dict(size=14, color=C_NO2, line=dict(color='white', width=2)),
        showlegend=False
    ))

    fig.add_annotation(
        x=str(dia_no2),
        y=val_no2,
        text="Pico de tráfico",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        bgcolor='white',
        bordercolor=C_NO2,
        font=dict(color=C_NO2)
    )

    # Highlight O3
    fig.add_trace(go.Scatter(
        x=[str(dia_o3)],
        y=[val_o3],
        mode='markers',
        marker=dict(size=14, color=C_O3, line=dict(color='white', width=2)),
        showlegend=False
    ))

    fig.add_annotation(
        x=str(dia_o3),
        y=val_o3,
        text="Peor aire (Ozono)",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        bgcolor='white',
        bordercolor=C_O3,
        font=dict(color=C_O3)
    )

    fig.update_layout(
        **PLOTLY_BASE,
        height=400,
        hovermode='x unified',
        showlegend=False,
        yaxis=dict(title='Nivel relativo (0–100)', range=[-5, 110])
    )

    return fig


@app.callback(
    Output('ranking-dias', 'figure'),
    Input('selector-contaminante', 'value'),
)
def render_ranking(contaminante):
    CONFIG = {
        'NO2': {
            'archivo':    'viz1_barras_no2.csv',
            'col_valor':  'NO2_ppb',
            'color_rgba': (44, 110, 158),  # Azul verdoso
            'color_hex':  '#2c6e9e',
            'label':      'NO₂ (ppb) — más alto = más tráfico',
            'titulo':     '🔵 Ranking de tráfico: ¿qué día hay más autos?',
        },
        'O3': {
            'archivo':    'viz3_ranking_dias_o3.csv',
            'col_valor':  'O3_promedio',
            'color_rgba': (212, 160, 23),  # Mostaza
            'color_hex':  '#d4a017',
            'label':      'Ozono (ppb) — más alto = más irritación',
            'titulo':     '🟠 Ranking de Ozono: ¿qué día respiramos peor?',
        },
        'PM25': {
            'archivo':    None,
            'col_valor':  None,
            'color_rgba': (192, 90, 59),   # Terracota
            'color_hex':  '#c05a3b',
            'label':      'PM2.5 (µg/m³) — más alto = más partículas dañinas',
            'titulo':     '🔴 Ranking de PM2.5: ¿qué día hay más partículas finas?',
        },
    }

    cfg = CONFIG[contaminante]

    if contaminante == 'NO2':
        df_rank = df_barras.groupby('Dia')['NO2_ppb'].mean().reset_index()
        df_rank.columns = ['Dia', 'valor']

    elif contaminante == 'O3':
        df_rank = df_ranking.copy()
        df_rank = df_rank[['Dia', 'O3_promedio']]
        df_rank.columns = ['Dia', 'valor']

    else:
        df_rank = df_pm25_precargado.groupby('Dia')['value'].mean().reset_index()
        df_rank.columns = ['Dia', 'valor']

    df_rank['Dia'] = pd.Categorical(df_rank['Dia'], categories=DIAS_ORDEN, ordered=True)
    df_rank = df_rank.sort_values('Dia')

    r, g, b = cfg['color_rgba']
    max_val = df_rank['valor'].max()
    min_val = df_rank['valor'].min()

    def t(v):
        return (v - min_val) / (max_val - min_val) if max_val != min_val else 0.5

    peor_dia = str(df_rank.loc[df_rank['valor'].idxmax(), 'Dia'])
    peor_val = df_rank['valor'].max()

    colores = []
    for v, dia in zip(df_rank['valor'], df_rank['Dia']):
        if str(dia) == str(peor_dia):
            colores.append(cfg['color_hex'])  
        else:
            colores.append(f'rgba({r},{g},{b},0.35)')


    fig = go.Figure(go.Bar(
        x=df_rank['valor'],
        y=df_rank['Dia'].astype(str),
        orientation='h',
        marker=dict(color=colores, line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>Promedio: <b>%{x:.1f}</b><extra></extra>",
        text=df_rank['valor'].round(1).astype(str),
        textposition='outside',
        textfont=dict(color=C_MUTED, size=12),
    ))

    fig.add_annotation(
    text="         ⬅ Peor día",
    x=peor_val,
    y=peor_dia,
    showarrow=False,
    xanchor='left',
    font=dict(color=cfg['color_hex'], size=15, family=FONT_BODY, weight='bold'),
    )
    fig.add_annotation(
    text="Escala fija (0–50) para comparar contaminantes",
    x=25,  
    y=1.15,
    xref='x',
    yref='paper',
    showarrow=False,
    font=dict(size=11, color=C_MUTED),
    )

    layout = {**PLOTLY_BASE, **dict(
        title=dict(text=cfg['titulo'], font=dict(size=14, color=C_MUTED), x=0),
        height=380,
        xaxis=dict(
            gridcolor=C_GRID,
            tickfont=dict(color=C_MUTED),
            title=cfg['label'],
            range=[0, 50],
        ),
        yaxis=dict(
            gridcolor=C_GRID,
            tickfont=dict(color=C_TEXT, size=13),
            title='',
            autorange='reversed',
        ),
        margin=dict(l=48, r=80, t=48, b=48),
    )}
    fig.update_layout(**layout)
    return fig


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)