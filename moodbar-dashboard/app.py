import os
import warnings

import mysql.connector
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# pandas prévient qu'il ne teste officiellement que SQLAlchemy pour read_sql ;
# mysql-connector fonctionne correctement ici, l'avertissement est sans impact
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

st.set_page_config(page_title="Moodbar — Dashboard", page_icon="🙂")

MOODS = ["content", "neutre", "pas_content"]
MOOD_LABELS = {"content": "🙂 Content", "neutre": "😐 Neutre", "pas_content": "🙁 Pas content"}


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
st.bar_chart(counts.rename(MOOD_LABELS))

st.subheader("Évolution dans le temps")
period = st.radio("Granularité", ["Jour", "Semaine", "Mois"], horizontal=True)
freq = {"Jour": "D", "Semaine": "W", "Mois": "ME"}[period]
trend = (
    filtered.groupby([pd.Grouper(key="horodatage", freq=freq), "humeur"])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=MOODS, fill_value=0)
    .rename(columns=MOOD_LABELS)
)
st.line_chart(trend)

st.subheader("Détail des votes")
st.dataframe(filtered.sort_values("horodatage", ascending=False), use_container_width=True)
