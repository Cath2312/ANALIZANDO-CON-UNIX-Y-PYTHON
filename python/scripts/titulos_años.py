import sys
import os

# Agregar el directorio base al PYTHONPATH
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_dir)
from imdb.movie_details_fetcher import (
    read_movie_urls, 
    read_and_sort_average_ratings, 
    get_top_bottom_movies, 
    get_movie_details_from_url
)

def fetch_movie_details(ratings_file, output_file, desired_count=10, ascending=False):
    # Leer y ordenar calificaciones promedio
    avg_ratings = read_and_sort_average_ratings(ratings_file)

    # Procesar las mejores o peores películas según el orden
    movie_details = []
    seen_movies = set()

    if ascending:
        avg_ratings = avg_ratings[::-1]  # Invertir para orden de menor a mayor

    for movie in avg_ratings:
        movie_id, avg_rating, url = movie
        title, year = get_movie_details_from_url(url)

        # Solo añadir si no se ha visto antes
        if (title, year) not in seen_movies:
            seen_movies.add((title, year))
            movie_details.append((title, year, avg_rating))

        # Salir si alcanzamos el número deseado
        if len(movie_details) >= desired_count:
            break

    # Guardar detalles en un archivo
    with open(output_file, 'w') as file:
        for title, year, avg_rating in movie_details:
            file.write(f"{title} ({year}) - Calificación promedio: {avg_rating}\n")

# Uso del script (si se ejecuta directamente)
if __name__ == "__main__":
    pos_ratings_file = './train/combined_pos.txt'
    neg_ratings_file = './train/combined_neg.txt'
    output_pos_file = './train/pos_movie_details.txt'
    output_neg_file = './train/neg_movie_details.txt'

    # Obtener películas positivas
    fetch_movie_details(pos_ratings_file, output_pos_file, desired_count=10, ascending=False)

    # Obtener películas negativas
    fetch_movie_details(neg_ratings_file, output_neg_file, desired_count=10, ascending=True)

    print(f"Detalles de películas positivas guardados en: {output_pos_file}")
    print(f"Detalles de películas negativas guardados en: {output_neg_file}")
