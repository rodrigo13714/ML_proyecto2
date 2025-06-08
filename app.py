import streamlit as st
import pandas as pd
import os
from PIL import Image

# Configuración general
st.set_page_config(page_title="🎬 Recomendador Visual", layout="wide")

# === Estilos personalizados ===
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: #222222;
            font-family: 'Segoe UI', sans-serif;
        }
        .block-title {
            font-size: 28px;
            font-weight: bold;
            margin-top: 10px;
            color: #0A2647;
        }
        .section {
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 20px;
            padding-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# === Título principal ===
st.markdown("<div class='block-title'>🎬 Recomendador de Películas por Póster</div>", unsafe_allow_html=True)
st.markdown("<div class='section'>Selecciona una película para ver sus recomendaciones visuales.</div>", unsafe_allow_html=True)

# === Cargar dataset ===
@st.cache_data
def load_data():
    return pd.read_csv("Recomendaciones_Limpio.csv")

df = load_data()

# === Selector de película ===
peliculas_unicas = df['query_movie_id'].drop_duplicates().sort_values().tolist()
selected_id = st.selectbox("🎞️ Elige el ID de una película:", peliculas_unicas)

# === Mostrar película seleccionada ===
st.markdown("<div class='block-title'>🎥 Película seleccionada</div>", unsafe_allow_html=True)
poster_path = f"posters/{selected_id}.jpg"
col1, col2 = st.columns([1, 2])

with col1:
    if os.path.exists(poster_path):
        st.image(Image.open(poster_path), width=250)
    else:
        st.warning("📭 Póster no encontrado en carpeta `posters/`")

with col2:
    st.write(f"**Movie ID:** `{selected_id}`")
    st.write("A continuación verás las 10 películas visualmente más similares.")

# === Recomendaciones ===
st.markdown("<div class='block-title'>🍿 Películas Recomendadas</div>", unsafe_allow_html=True)
recomendaciones = df[df['query_movie_id'] == selected_id].sort_values('position')

cols = st.columns(5)
for idx, (_, row) in enumerate(recomendaciones.iterrows()):
    col = cols[idx % 5]
    with col:
        rec_id = row['recommended_movie_id']
        rec_title = row['title']
        rec_genre = row['genre']
        poster_rec_path = f"posters/{rec_id}.jpg"

        if os.path.exists(poster_rec_path):
            col.image(Image.open(poster_rec_path), width=140)
        else:
            col.caption("📭 Sin póster")

        col.markdown(f"<div style='font-weight:bold; font-size:14px'>{rec_title}</div>", unsafe_allow_html=True)
        col.caption(f"🎭 {rec_genre}")
