import streamlit as st
import pandas as pd

# ========================
# CONFIGURAÇÃO DA PÁGINA
# ========================
st.set_page_config(
    page_title="Hábitos Musicais — Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# AJUSTE DE LARGURA DO SIDEBAR
# ========================
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            min-width: 320px;
            max-width: 320px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ========================
# TEMA (DARK MODE)
# ========================
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========================
# TÍTULO
# ========================
st.title("🎧 Dashboard de Hábitos Musicais")
st.caption("Exploração interativa dos hábitos de escuta ao longo do tempo")

# ========================
# CARREGAMENTO DOS DADOS DE ESCUTA
# ========================
@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/scrobbles_dashboard_time_enriched.csv"
    )

df = load_data()

# Garantir datetime sem timezone (já em horário local)
df["played_at_br"] = pd.to_datetime(df["played_at_br"]).dt.tz_localize(None)

# ========================
# SIDEBAR — FILTROS
# ========================
st.sidebar.header("🎛️ Filtros")

# Datas mínimas e máximas do dataset
min_date = pd.to_datetime(df["played_at_br"]).min().date()
max_date = pd.to_datetime(df["played_at_br"]).max().date()

def year_range(year):
    start = max(min_date, pd.to_datetime(f"{year}-01-01").date())
    end = min(max_date, pd.to_datetime(f"{year}-12-31").date())
    return (start, end)

# ========================
# PERÍODO
# ========================
st.sidebar.subheader("📅 Período")

col1, col2, col3, col4 = st.sidebar.columns(4)

# Valor padrão do intervalo
date_range = (min_date, max_date)

with col1:
    if st.button("2023"):
        date_range = year_range(2023)

with col2:
    if st.button("2024"):
        date_range = year_range(2024)

with col3:
    if st.button("2025"):
        date_range = year_range(2025)

with col4:
    if st.button("Tudo"):
        date_range = (min_date, max_date)

date_range = st.sidebar.date_input(
    "Selecionar intervalo",
    value=date_range,
    min_value=min_date,
    max_value=max_date
)

# ========================
# FILTRO DE GÊNERO MUSICAL
# ========================
st.sidebar.subheader("🎵 Gêneros musicais")

available_genres = (
    df["macro_genre"]
    .dropna()
    .sort_values()
    .unique()
    .tolist()
)

selected_genres = st.sidebar.multiselect(
    "Filtrar por gênero",
    options=available_genres,
    default=available_genres
)


# ========================
# APLICAR FILTROS
# ========================
df_filtered = df.copy()

# Filtro de data
if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_filtered[
        (df_filtered["played_at_br"] >= pd.to_datetime(start_date)) &
        (df_filtered["played_at_br"] <= pd.to_datetime(end_date))
    ]

# Filtro de gênero
if selected_genres:
    df_filtered = df_filtered[
        df_filtered["macro_genre"].isin(selected_genres)
    ]

# ========================
# KPIs — TOPO
# ========================
col1, col2, col3, col4 = st.columns(4)

# KPI 1 — Total de reproduções
with col1:
    st.metric(
        label="🎧 Total de reproduções",
        value=f"{len(df_filtered):,}"
    )

# KPI 2 — Gênero predominante
with col2:
    top_genre = (
        df_filtered["macro_genre"]
        .value_counts()
        .idxmax()
        if not df_filtered.empty else "-"
    )
    st.metric(
        label="🎵 Gênero predominante",
        value=top_genre.capitalize()
    )

# KPI 3 — Energia predominante
with col3:
    top_energy = (
        df_filtered["energy_level"]
        .value_counts()
        .idxmax()
        if not df_filtered.empty else "-"
    )
    st.metric(
        label="⚡ Energia predominante",
        value=top_energy.capitalize()
    )

# KPI 4 — Estado emocional predominante
with col4:
    mood_series = (
        df_filtered["mood"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    top_mood = (
        mood_series.value_counts().idxmax()
        if not mood_series.empty else "-"
    )

    st.metric(
        label="🌈 Estado emocional predominante",
        value=top_mood.capitalize()
    )


# ========================
# RANKINGS
# ========================
st.subheader("🏆 Rankings do período selecionado")

col_a, col_b, col_c = st.columns(3)

# ------------------------
# TOP ARTISTAS
# ------------------------
with col_a:
    st.markdown("### 🎤 Top Artistas")

    top_artists = (
        df_filtered
        .groupby("artist_clean")
        .size()
        .sort_values(ascending=False)
        .head(5)
        .reset_index(name="Reproduções")
        .rename(columns={"artist_clean": "Artista"})
    )

    st.dataframe(
        top_artists,
        use_container_width=True,
        hide_index=True
    )

# ------------------------
# TOP ÁLBUNS
# ------------------------
with col_b:
    st.markdown("### 💿 Top Álbuns")

    top_albums = (
        df_filtered
        .groupby(["album", "artist_clean"])
        .size()
        .sort_values(ascending=False)
        .head(5)
        .reset_index(name="Reproduções")
        .rename(columns={
            "album": "Álbum",
            "artist_clean": "Artista"
        })
    )

    st.dataframe(
        top_albums,
        use_container_width=True,
        hide_index=True
    )

# ------------------------
# TOP MÚSICAS
# ------------------------
with col_c:
    st.markdown("### 🎶 Top Músicas")

    top_tracks = (
        df_filtered
        .groupby(["track", "artist_clean"])
        .size()
        .sort_values(ascending=False)
        .head(5)
        .reset_index(name="Reproduções")
        .rename(columns={
            "track": "Música",
            "artist_clean": "Artista"
        })
    )

    st.dataframe(
        top_tracks,
        use_container_width=True,
        hide_index=True
    )


# ========================
# CONTROLE DO STREAMGRAPH
# ========================

stream_metric = st.radio(
    "Agrupar por:",
    ["Gênero", "Mood", "Energia"],
    horizontal=True
)

if stream_metric == "Gênero":
    category_col = "macro_genre"
elif stream_metric == "Mood":
    category_col = "mood"
else:
    category_col = "energy_level"


# ========================
# STREAMGRAPH — PREPARAÇÃO
# ========================

df_filtered["year_month"] = df_filtered["played_at_br"].dt.to_period("M").astype(str)

# Explodir mood (caso selecionado)
df_stream = df_filtered.copy()

if category_col == "mood":
    df_stream = df_stream.assign(
        mood=df_stream["mood"].str.split(", ")
    ).explode("mood")

stream_time = (
    df_stream
    .groupby(["year_month", category_col])
    .size()
    .reset_index(name="reproduções")
)

# Pivot para formato largo
pivot = stream_time.pivot(
    index="year_month",
    columns=category_col,
    values="reproduções"
).fillna(0)

# Ordem das categorias (reduz cruzamentos)
category_order = pivot.mean().sort_values().index

# Soma total por mês
total = pivot.sum(axis=1)

# Baseline (centro do streamgraph)
baseline = -total / 2


# ========================
# STREAMGRAPH — EVOLUÇÃO DA ESCUTA AO LONGO DO TEMPO
# ========================

import plotly.graph_objects as go

st.subheader(f"🎶 Evolução da escuta ao longo do tempo — por {stream_metric.lower()}")

fig = go.Figure()

current = baseline.copy()

for category in category_order:
    values = pivot[category]

    fig.add_trace(
        go.Scatter(
            x=pivot.index,
            y=current + values,
            mode="lines",
            fill="tonexty",
            name=str(category).capitalize(),
            hovertemplate=(
                "<b>%{x}</b><br>"
                f"{stream_metric} predominante: {str(category).capitalize()}<br>"
                "Reproduções: %{y}<extra></extra>"
            )
        )
    )

    current += values

fig.update_layout(
    template="plotly_dark",
    hovermode="x unified",
    xaxis_title="",
    yaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        x=1.02,
        y=0.5,
        xanchor="left",
        yanchor="middle",
        bgcolor="rgba(0,0,0,0)"
    )
)

st.plotly_chart(fig, use_container_width=True)


# ========================
# CONTROLE DO HEATMAP
# ========================

heatmap_metric = st.radio(
    "Analisar por:",
    ["Volume", "Mood", "Energia"],
    horizontal=True
)

# ========================
# HEATMAP — PREPARAÇÃO
# ========================

df_heat = df_filtered.copy()

df_heat["hour"] = df_heat["played_at_br"].dt.hour
df_heat["weekday"] = df_heat["played_at_br"].dt.day_name(locale="pt_BR")

weekday_order = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo"
]

df_heat["weekday"] = pd.Categorical(
    df_heat["weekday"],
    categories=weekday_order,
    ordered=True
)

if heatmap_metric == "Volume":
    heatmap_matrix = (
        df_heat
        .groupby(["weekday", "hour"])
        .size()
        .unstack(fill_value=0)
    )

elif heatmap_metric == "Energia":
    heatmap_matrix = (
        df_heat
        .groupby(["weekday", "hour"])["energy_level"]
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        .unstack()
    )

else:
    df_mood = df_heat.copy()
    df_mood["mood"] = df_mood["mood"].str.split(", ")
    df_mood = df_mood.explode("mood")

    heatmap_matrix = (
        df_mood
        .groupby(["weekday", "hour"])["mood"]
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        .unstack()
    )

import plotly.graph_objects as go

st.subheader(
    f"🕒 Padrão de escuta por hora e dia da semana ({heatmap_metric.lower()})"
)

# ========================
# HEATMAP — VOLUME
# ========================
if heatmap_metric == "Volume":

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=heatmap_matrix.values,
            x=heatmap_matrix.columns,
            y=heatmap_matrix.index,
            colorscale=[
                [0.0,  "rgba(0,255,0,0.05)"],
                [0.25, "rgba(0,255,0,0.20)"],
                [0.5,  "rgba(0,255,0,0.45)"],
                [0.75, "rgba(0,255,0,0.75)"],
                [1.0,  "rgba(0,255,0,1.0)"]
            ],
            colorbar=dict(
                title="Atividade",
                tickvals=[],
                len=0.6,
                thickness=12,
                outlinewidth=0
            ),
            hovertemplate=(
                "Dia: %{y}<br>"
                "Hora: %{x}h<br>"
                "Reproduções: %{z}<extra></extra>"
            )
        )
    )

# ========================
# HEATMAP — ENERGIA
# ========================
elif heatmap_metric == "Energia":

    energy_map = {
        "low": 0,
        "medium": 1,
        "high": 2
    }

    z = heatmap_matrix.replace(energy_map).values

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=z,
            x=heatmap_matrix.columns,
            y=heatmap_matrix.index,
            colorscale=[
                [0.0, "rgba(255, 214, 0, 0.15)"],
                [0.5, "rgba(255, 214, 0, 0.45)"],
                [1.0, "rgba(255, 214, 0, 0.90)"]
            ],
            colorbar=dict(
                title="Energia",
                tickvals=[0, 1, 2],
                ticktext=["Baixa", "Média", "Alta"],
                len=0.6,
                thickness=12,
                outlinewidth=0
            ),
            hovertemplate=(
                "Dia: %{y}<br>"
                "Hora: %{x}h<br>"
                "Energia predominante: %{z}<extra></extra>"
            )
        )
    )

# ========================
# HEATMAP — MOOD (CATEGÓRICO)
# ========================
else:

    mood_colors = {
        "calm": "rgba(59, 130, 246, 0.45)",
        "chill": "rgba(6, 182, 212, 0.45)",
        "happy": "rgba(250, 204, 21, 0.50)",
        "energetic": "rgba(249, 115, 22, 0.55)",
        "aggressive": "rgba(239, 68, 68, 0.55)"
    }

    mood_map = {mood: i for i, mood in enumerate(mood_colors.keys())}
    z = heatmap_matrix.replace(mood_map).values

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=z,
            x=heatmap_matrix.columns,
            y=heatmap_matrix.index,
            colorscale=[
                [i / (len(mood_colors) - 1), color]
                for i, color in enumerate(mood_colors.values())
            ],
            showscale=False,
            hovertemplate=(
                "Dia: %{y}<br>"
                "Hora: %{x}h<br>"
                "Estado emocional predominante: %{text}<extra></extra>"
            ),
            text=heatmap_matrix.values
        )
    )

    # Legenda categórica do mood
    for mood, color in mood_colors.items():
        fig_heat.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=10, color=color),
                name=mood.capitalize(),
                showlegend=True
            )
        )

# ========================
# LAYOUT FINAL
# ========================

fig_heat.update_layout(
    showlegend=True,
    legend_title_text="Estado emocional predominante",
    template="plotly_dark",
    xaxis=dict(tickmode="linear", dtick=1, zeroline=False),
    yaxis=dict(zeroline=False),
    margin=dict(l=60, r=20, t=40, b=40)
)

st.plotly_chart(fig_heat, use_container_width=True)


# ========================
# TABELA (DEBUG / SANITY CHECK)
# ========================
with st.expander("🔍 Ver amostra dos dados"):
    st.dataframe(df_filtered.head(20))
