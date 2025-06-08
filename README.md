# 🎬 Recomendador Visual de Películas

Este proyecto es una aplicación web construida con **Streamlit** que permite al usuario obtener recomendaciones de películas basadas en la similitud visual de sus pósters. A partir de una película seleccionada por su ID, el sistema muestra sugerencias visuales de títulos relacionados.

## 📁 Estructura del Proyecto


### posters/                    Carpeta con los pósters de películas
### posters_test/               Carpeta con pósters para pruebas
### Recomendaciones_Limpio.csv  Dataset limpio con 29,231 filas de recomendaciones, este el submission de kaggle pero se le fueron agregadas 4 columnas, ya que solo se conocia el ID y la posicion, se le agregaron ### columnas para tener el titulo y genero de la pelicula recomendada o la relacionada. De esta manera para que se pueda mostrar correctamente la pelicula con su ID, titulo y genero.
### app.py                      Código principal de la app en Streamlit
### requirements.txt            Dependencias necesarias para ejecutar la app
