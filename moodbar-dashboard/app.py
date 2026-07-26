import os
import warnings

import mysql.connector
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# pandas prévient qu'il ne teste officiellement que SQLAlchemy pour read_sql ;
# mysql-connector fonctionne correctement ici, l'avertissement est sans impact
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

st.set_page_config(page_title="Moodbar — Dashboard", page_icon="🙂")

# mêmes couleurs que moodbar-frontend/style.css (bordures des mood-btn), pour une identité
# visuelle cohérente entre le vote et le dashboard
MOODS = ["content", "neutre", "pas_content"]
MOOD_LABELS = {"content": "🙂 Content", "neutre": "😐 Neutre", "pas_content": "🙁 Pas content"}
MOOD_COLORS = {"content": "#4caf7d", "neutre": "#e0b23d", "pas_content": "#e2685f"}

# thème carte pour les st.metric + fond de page, dans l'esprit du mockup fourni
st.markdown(
    """
    <style>
    .stApp { background-color: #f7f5f2; }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e8e4dd;
        border-radius: 0.75rem;
        padding: 1rem 1rem 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "moodbar"),
    )


@st.cache_data(ttl=30)
def load_votes():
    conn = get_connection()
    df = pd.read_sql("SELECT humeur, horodatage, source FROM votes", conn)
    conn.close()
    return df


st.title("🙂😐🙁 Moodbar — Dashboard analytique")

if st.button("Actualiser"):
    st.cache_data.clear()

df = load_votes()

if df.empty:
    st.info("Aucun vote enregistré pour le moment.")
    st.stop()

df["horodatage"] = pd.to_datetime(df["horodatage"])

min_date = df["horodatage"].min().date()
max_date = df["horodatage"].max().date()
date_range = st.date_input("Période", value=(min_date, max_date), min_value=min_date, max_value=max_date)
start, end = date_range if isinstance(date_range, tuple) and len(date_range) == 2 else (date_range, date_range)

filtered = df[(df["horodatage"].dt.date >= start) & (df["horodatage"].dt.date <= end)]

st.subheader("Répartition globale des humeurs")
counts = filtered["humeur"].value_counts().reindex(MOODS, fill_value=0)
col1, col2, col3 = st.columns(3)
for col, mood in zip((col1, col2, col3), MOODS):
    col.metric(MOOD_LABELS[mood], counts[mood])

# le donut porte lui-même le libellé + pourcentage sur chaque part (pas seulement la couleur) :
# cf. vérification d'accessibilité couleur (voir résumé) — neutre/pas_content se confondent
# en deutéranopie, donc l'identité ne doit jamais reposer sur la seule teinte
donut = go.Figure(
    data=[
        go.Pie(
            labels=[MOOD_LABELS[m] for m in MOODS],
            values=[counts[m] for m in MOODS],
            hole=0.55,
            sort=False,
            direction="clockwise",
            marker=dict(colors=[MOOD_COLORS[m] for m in MOODS], line=dict(color="#ffffff", width=2)),
            textinfo="percent",
            textposition="outside",
            hovertemplate="%{label}<br>%{value} votes (%{percent})<extra></extra>",
        )
    ]
)
donut.update_layout(
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#6b6b6b"),
    margin=dict(t=10, b=10, l=10, r=10),
)
st.plotly_chart(donut, use_container_width=True)

st.subheader("Évolution dans le temps")
period = st.radio("Granularité", ["Jour", "Semaine", "Mois"], horizontal=True)
freq = {"Jour": "D", "Semaine": "W", "Mois": "ME"}[period]
trend = (
    filtered.groupby([pd.Grouper(key="horodatage", freq=freq), "humeur"])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=MOODS, fill_value=0)
)

bars = go.Figure()
for mood in MOODS:
    bars.add_trace(
        go.Bar(
            x=trend.index,
            y=trend[mood],
            name=MOOD_LABELS[mood],
            marker=dict(color=MOOD_COLORS[mood]),
            hovertemplate="%{y} votes<extra>" + MOOD_LABELS[mood] + "</extra>",
        )
    )
bars.update_layout(
    barmode="group",
    bargap=0.25,
    bargroupgap=0.08,
    hovermode="x unified",
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#6b6b6b"),
    margin=dict(t=40, b=10, l=10, r=10),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#eceae5", zeroline=False),
)
st.plotly_chart(bars, use_container_width=True)

st.subheader("Détail des votes")
st.dataframe(filtered.sort_values("horodatage", ascending=False), use_container_width=True)
