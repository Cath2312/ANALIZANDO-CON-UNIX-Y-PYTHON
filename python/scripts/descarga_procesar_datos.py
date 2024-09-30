import sys
import os
import shutil

# Agregar el directorio base al PYTHONPATH
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_dir)

from imdb.downloader import download_file
from imdb.extractor import extract_file
from imdb.rating_extractor import extract_ratings_from_files
from imdb.url_rating_combiner import combine_urls_and_ratings

# Código principal
url = 'https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz'
destination = 'aclImdb_v1.tar.gz'
temp_extract_path = 'temp_aclImdb'
final_extract_path = 'aclImdb'

# Descargar el archivo
download_file(url, destination)

# Extraer en un directorio temporal
extract_file(destination, temp_extract_path)

# Verificar que la carpeta extraída exista y mover archivos
src_dir = os.path.join(temp_extract_path, 'aclImdb')
if os.path.exists(src_dir):
    if os.path.exists(final_extract_path):
        shutil.rmtree(final_extract_path)  # Eliminar la carpeta final si ya existe
    shutil.move(src_dir, final_extract_path)  # Mover la carpeta a la ubicación final
else:
    print("No se encontró la carpeta extraída.")

# Limpiar el directorio temporal
shutil.rmtree(temp_extract_path)

# Directorios para las calificaciones
train_dir = os.path.join(final_extract_path, 'train')
neg_dir = os.path.join(train_dir, 'neg')
pos_dir = os.path.join(train_dir, 'pos')

# Crear archivos de salida si no existen
combined_pos_file = './train/combined_pos.txt'
combined_neg_file = './train/combined_neg.txt'

if not os.path.exists('./train'):
    os.makedirs('./train')

# Extraer calificaciones de los directorios negativos y positivos
neg_ratings_file = './train/neg_ratings.txt'
pos_ratings_file = './train/pos_ratings.txt'

if os.path.exists(neg_dir):
    extract_ratings_from_files(neg_dir, neg_ratings_file)

if os.path.exists(pos_dir):
    extract_ratings_from_files(pos_dir, pos_ratings_file)

# Combinar URLs y calificaciones
urls_pos_file = os.path.join(train_dir, 'urls_pos.txt')
urls_neg_file = os.path.join(train_dir, 'urls_neg.txt')

combine_urls_and_ratings(urls_pos_file, pos_ratings_file, combined_pos_file)
combine_urls_and_ratings(urls_neg_file, neg_ratings_file, combined_neg_file)

# Filtrar y ordenar URLs y calificaciones
def get_sorted_unique_movies(input_file, positive=True):
    movies = set()
    
    with open(input_file, 'r') as infile:
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                url = parts[0]
                rating = float(parts[1])
                movies.add((url, rating))

    if positive:
        sorted_movies = sorted(movies, key=lambda x: x[1], reverse=True)[:10]  # Mejores 10
    else:
        sorted_movies = sorted(movies, key=lambda x: x[1])[:10]  # Peores 10
    
    return sorted_movies

# Obtener las mejores y peores películas
top_movies = get_sorted_unique_movies(combined_pos_file, positive=True)
worst_movies = get_sorted_unique_movies(combined_neg_file, positive=False)

# Guardar URLs y calificaciones en archivos
def save_sorted_movies(movies, output_file):
    with open(output_file, 'w') as outfile:
        for url, rating in movies:
            outfile.write(f"{url}\t{rating:.1f}\n")

save_sorted_movies(top_movies, './train/top_10_movies.txt')
save_sorted_movies(worst_movies, './train/worst_10_movies.txt')

print("Mejores películas guardadas en './train/top_10_movies.txt'.")
print("Peores películas guardadas en './train/worst_10_movies.txt'.")
