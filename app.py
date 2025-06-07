import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Recomendador de Películas", layout="wide")

# ==== Cargar datos ====
@st.cache_data
def load_data():
    df = pd.read_csv("recomendaciones_completo.csv")
    return df

df = load_data()

# === Interfaz de selección ===
st.title("🎬 Recomendador de Películas por Similitud Visual")
st.markdown("Selecciona una película del set de prueba para ver recomendaciones basadas en pósters.")

peliculas_unicas = df[['query_movie_id']].drop_duplicates().reset_index(drop=True)
df_test_info = df[['query_movie_id', 'title', 'genre']].drop_duplicates('query_movie_id')
titulo_default = df_test_info.iloc[0]['title']

pelicula_seleccionada = st.selectbox(
    "🎞️ Película de consulta:",
    df_test_info['title'].tolist(),
    index=0
)

# === Mostrar info película seleccionada ===
info = df_test_info[df_test_info['title'] == pelicula_seleccionada].iloc[0]
query_id = info['query_movie_id']
st.subheader(f"🎥 Película seleccionada: {pelicula_seleccionada}")
st.write(f"**ID:** {query_id}")
st.write(f"**Género:** {info['genre']}")

# === Función para mostrar poster ===
def mostrar_poster(movie_id, carpeta='posters', width=150):
    path = os.path.join(carpeta, f"{movie_id}.jpg")
    if os.path.exists(path):
        img = Image.open(path)
        st.image(img, width=width)
    else:
        st.write("📭 Póster no disponible")

# === Mostrar póster de película seleccionada ===
st.markdown("#### 🖼️ Póster de la película")
mostrar_poster(query_id, carpeta='posters_test', width=250)

# === Mostrar recomendaciones ===
st.markdown("### ✅ Películas Recomendadas")
recomendaciones = df[df['query_movie_id'] == query_id].sort_values('position')

cols = st.columns(5)
for idx, (_, row) in enumerate(recomendaciones.iterrows()):
    with cols[idx % 5]:
        mostrar_poster(row['recommended_movie_id'], carpeta='posters', width=120)
        st.markdown(f"**🎬 {row['title']}**")
        st.caption(f"📚 {row['genre']} | Pos: {row['position']}")
