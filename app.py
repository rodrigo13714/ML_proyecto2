import pandas as pd
import os
from PIL import Image
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="🎬 Recomendador Visual de Películas", layout="wide")

# Título principal
st.title("🎬 Recomendador Visual de Películas")
st.markdown("Selecciona una película y descubre 10 recomendaciones visualmente similares basadas en pósters.")

# Cargar los datos
@st.cache_data
def load_data():
    return pd.read_csv("Recomendaciones_Limpio.csv")

df = load_data()

# Obtener lista única de películas de entrada
peliculas_unicas = df[['query_movie_id', 'title']].drop_duplicates().sort_values('title')
peliculas_dict = dict(zip(peliculas_unicas['title'], peliculas_unicas['query_movie_id']))

# Selector de película
selected_title = st.selectbox("🎞️ Escoge una película:", list(peliculas_dict.keys()))
selected_id = peliculas_dict[selected_title]

st.markdown("---")

# Mostrar póster de la película seleccionada
st.subheader("🎥 Película Seleccionada")
poster_path = f"posters/{selected_id}.jpg"

col1, col2 = st.columns([1, 3])
with col1:
    if os.path.exists(poster_path):
        st.image(Image.open(poster_path), caption=selected_title, use_column_width=True)
    else:
        st.warning("📭 Póster no disponible.")

with col2:
    st.markdown(f"**🎬 Título:** {selected_title}")
    st.markdown(f"**🆔 ID:** `{selected_id}`")

st.markdown("---")
st.subheader("🍿 Recomendaciones Visuales")

# Obtener y mostrar recomendaciones
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
            col.image(Image.open(poster_rec_path), use_column_width=True)
        else:
            col.caption("📭 Sin póster")
        col.markdown(f"**{rec_title}**")
        col.caption(f"🎭 {rec_genre}")
