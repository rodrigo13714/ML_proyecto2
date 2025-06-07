import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(layout="wide")
st.title("🎬 Recomendador de Películas por Póster")

# === Cargar datos ===
@st.cache_data
def load_data():
    return pd.read_csv("recomendaciones_completo.csv")

df = load_data()

# === Lista única de películas para seleccionar ===
peliculas_query = df[['query_movie_id', 'title']].drop_duplicates().sort_values('title')

pelicula_seleccionada = st.selectbox(
    "Selecciona una película para ver sus recomendaciones:",
    peliculas_query['title'].tolist()
)

def mostrar_poster(movie_id, carpeta, width=150):
    ruta = os.path.join(carpeta, f"{movie_id}.jpg")
    if os.path.exists(ruta):
        img = Image.open(ruta)
        st.image(img, width=width)
    else:
        st.write("📭 Póster no disponible")

# === Mostrar información y recomendaciones ===
if pelicula_seleccionada:
    info = peliculas_query[peliculas_query['title'] == pelicula_seleccionada].iloc[0]
    query_id = info['query_movie_id']

    st.subheader("🎥 Película Seleccionada")
    mostrar_poster(query_id, "posters_test", width=250)

    info_peli = df[df['query_movie_id'] == query_id].iloc[0]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Título:** {info_peli['title']}")
        st.markdown(f"**Género:** {info_peli['genre']}")
    with col2:
        st.markdown(f"**Año:** {int(info_peli['year_test']) if not pd.isna(info_peli['year_test']) else 'N/A'}")
        st.markdown(f"**Votos:** {int(info_peli['vote_test']) if not pd.isna(info_peli['vote_test']) else 'N/A'}")

    st.subheader("🍿 Recomendaciones")
    recomendaciones = df[df['query_movie_id'] == query_id].sort_values('position')

    cols = st.columns(5)
    for idx, (_, row) in enumerate(recomendaciones.iterrows()):
        col = cols[idx % 5]
        with col:
            mostrar_poster(row['recommended_movie_id'], "posters", width=120)
            st.markdown(f"**{row['title_train']}**")
            st.caption(f"{row['genre_train']} ({int(row['year_train']) if not pd.isna(row['year_train']) else 'N/A'})")
            st.caption(f"⭐ Votos: {int(row['vote_train']) if not pd.isna(row['vote_train']) else 'N/A'}")
