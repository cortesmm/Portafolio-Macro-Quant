import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Portafolio Global Macro", page_icon="📈", layout="wide")

st.title("📈 Análisis Cuantitativo: Estrategia Top-Down Global Macro")
st.markdown("""
Esta aplicación reconstruye el rendimiento histórico de un portafolio real basado en tesis de megatendencias (IA, Transición Energética) y coberturas geopolíticas, **anonimizando los montos de inversión mediante rentabilidad porcentual**.
""")
st.divider()

# ==========================================
# CARGA DE DATOS
# ==========================================
@st.cache_data
def load_data():
    df_rend = pd.read_csv('rendimiento_portafolio.csv', parse_dates=['Date'])
    df_trans = pd.read_csv('transacciones_limpias.csv')
    return df_rend, df_trans

df_rend, df_trans = load_data()

# ==========================================
# SECCIÓN 1: KPIs INSTITUCIONALES (Sin Montos)
# ==========================================
st.subheader("Resumen de Desempeño (Métricas Relativas)")

ultimo_dia = df_rend.iloc[-1]
rendimiento_total = ultimo_dia['Rendimiento_%']

col1, col2, col3 = st.columns(3)
col1.metric("Estatus del Capital", "Activo y Gestionado")
col2.metric("Rendimiento Acumulado", f"{rendimiento_total:.2f}%", "Generación de Alfa (+)")
col3.metric("Perfil de Riesgo", "Diversificación Temática")

st.divider()

# ==========================================
# SECCIÓN 2: GRÁFICA DE RENDIMIENTO + ANOTACIONES MACRO
# ==========================================
st.subheader("Curva de Rendimiento Acumulado y Eventos Macro")

fig_line = go.Figure()

# Graficamos directamente el porcentaje de rendimiento (Línea principal)
fig_line.add_trace(go.Scatter(
    x=df_rend['Date'], y=df_rend['Rendimiento_%'],
    mode='lines', name='Rendimiento del Portafolio (%)',
    line=dict(color='#00FA9A', width=3),
    fill='tozeroy', fillcolor='rgba(0, 250, 154, 0.1)'
))

# --- EVENTOS MACROECONÓMICOS (Anotaciones Verticales) ---
eventos_macro = [
    {"fecha": "2025-06-20", "texto": "Tesis IA/Nuclear<br>(NVDA, MU, NLR)"},
    {"fecha": "2025-07-07", "texto": "Aceleración Growth<br>Anticipando Earnings"},
    {"fecha": "2025-09-02", "texto": "DCA Condicional<br>(NFP / CPI)"},
    {"fecha": "2025-12-19", "texto": "Consolidación<br>Fin de Año"}
]

for evento in eventos_macro:
    # Agregamos línea vertical
    fig_line.add_vline(x=evento["fecha"], line_width=1.5, line_dash="dash", line_color="#FFA500")
    # Agregamos texto explicativo
    fig_line.add_annotation(
        x=evento["fecha"], y=df_rend['Rendimiento_%'].max() * 0.9, 
        text=evento["texto"], showarrow=False, 
        font=dict(color="#FFA500", size=10),
        bgcolor="rgba(0,0,0,0.5)", bordercolor="#FFA500", borderpad=4,
        xanchor="left", yanchor="top"
    )

fig_line.update_layout(
    xaxis_title="Fecha de Mercado",
    yaxis_title="Rendimiento Acumulado (%)",
    hovermode="x unified",
    template="plotly_dark",
    height=550,
    yaxis=dict(ticksuffix="%")
)

st.plotly_chart(fig_line, use_container_width=True)

# ==========================================
# SECCIÓN 3: COMPOSICIÓN DEL PORTAFOLIO (En Porcentajes)
# ==========================================
st.subheader("Composición Táctica Actual")

df_trans['Monto_Invertido'] = df_trans['Titulos'] * df_trans['Precio_Ejecucion']
df_distribucion = df_trans[df_trans['Accion'].str.lower() == 'buy'].groupby('Ticker')['Monto_Invertido'].sum().reset_index()

# Convertimos a Porcentajes para no mostrar dinero
total_invertido = df_distribucion['Monto_Invertido'].sum()
df_distribucion['Peso_%'] = (df_distribucion['Monto_Invertido'] / total_invertido) * 100

fig_pie = px.pie(
    df_distribucion, 
    values='Peso_%', 
    names='Ticker', 
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Teal
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_pie.update_layout(template="plotly_dark")

st.plotly_chart(fig_pie, use_container_width=True)
