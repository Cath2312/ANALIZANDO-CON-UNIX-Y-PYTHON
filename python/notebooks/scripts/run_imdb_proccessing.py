import os
import requests
import tarfile
import stat
import datetime
import pandas as pd
import re
import json
from bs4 import BeautifulSoup

# Función para descargar el archivo
def download_file(url, destination):
    if not os.path.exists(destination):
        response = requests.get(url, stream=True)
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Archivo descargado: {destination}")
    else:
        print(f"El archivo ya existe: {destination}")

# Función para extraer el archivo
def extract_file(tar_path, extract_path):
    if not os.path.exists(extract_path):
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall(path=extract_path)
        print(f"Archivo descomprimido en: {extract_path}")
    else:
        print(f"El directorio ya existe: {extract_path}")

# Función para imprimir la estructura del directorio
def print_directory_structure(path, indent=0, max_files=10):
    try:
        entries = sorted(os.listdir(path))
        if len(entries) > max_files:
            print(' ' * indent + '...un montón de archivos...')
        else:
            for entry in entries:
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    print(' ' * indent + f'{entry}/')
                    print_directory_structure(full_path, indent + 1, max_files)
                else:
                    print(' ' * indent + entry)
    except PermissionError:
        print(' ' * indent + 'Permiso denegado')

# Función para extraer información del archivo
def print_file_info(file_path):
    try:
        file_stat = os.stat(file_path)
        size = file_stat.st_size
        size_rep = f'{size} bytes' if size < 1024 else f'{size / 1024:.2f} KiB' if size < 1048576 else f'{size / 1048576:.2f} MiB'
        permissions = stat.filemode(file_stat.st_mode)
        print(f'Nombre completo: {file_path}')
        print(f'Ruta absoluta: {os.path.abspath(file_path)}')
        print(f'Tipo: {"Directorio" if os.path.isdir(file_path) else "Archivo regular"}')
        print(f'Tamaño: {size} bytes ({size_rep})')
        print(f'Permisos: {permissions}')
        print(f'Último acceso: {datetime.datetime.fromtimestamp(file_stat.st_atime)}')
        print(f'Última modificación: {datetime.datetime.fromtimestamp(file_stat.st_mtime)}')
        print(f'Fecha de creación: {datetime.datetime.fromtimestamp(file_stat.st_ctime)}')
    except FileNotFoundError:
        print(f'Archivo no encontrado: {file_path}')

# Función para extraer calificaciones de los archivos
def extract_ratings_from_files(directory, output_file):
    try:
        with open(output_file, 'w') as outfile:
            for file_name in os.listdir(directory):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(directory, file_name)
                    base_name = os.path.splitext(file_name)[0]
                    try:
                        movie_id, rating = map(int, base_name.split('_'))
                        outfile.write(f'{rating}\n')
                    except ValueError:
                        print(f'Error al procesar el archivo {file_name}: nombre de archivo no válido.')
        print(f'Calificaciones extraídas y guardadas en {output_file}')
    except Exception as e:
        print(f'Error al procesar el directorio {directory}: {e}')

# Función para combinar URLs y calificaciones
def combine_urls_and_ratings(url_file, rating_file, output_file):
    try:
        with open(url_file, 'r') as urls, open(rating_file, 'r') as ratings, open(output_file, 'w') as outfile:
            url_lines = urls.readlines()
            rating_lines = ratings.readlines()
            if len(url_lines) != len(rating_lines):
                raise ValueError(f'El número de líneas en {url_file} y {rating_file} no coincide.')
            for url_line, rating_line in zip(url_lines, rating_lines):
                url = url_line.strip()
                rating = rating_line.strip()
                outfile.write(f'{url}\t{rating}\n')
        print(f'URLs y calificaciones combinadas y guardadas en {output_file}')
    except Exception as e:
        print(f'Error al procesar los archivos: {e}')

# Función para calcular las calificaciones promedio
def average_ratings(input_file, output_file):
    try:
        df = pd.read_csv(input_file, sep='\t', header=None, names=['url', 'rating'])
        df['rating'] = df['rating'].astype(float)
        avg_df = df.groupby('url').agg({'rating': 'mean'}).reset_index()
        avg_df.to_csv(output_file, index=False, sep='\t', header=False)
        print(f'Calificaciones promedio guardadas en {output_file}')
    except Exception as e:
        print(f'Error al procesar el archivo: {e}')

# Función para imprimir las mejores y peores películas
def print_top_10_movies(input_file, worst=False):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
        movie_data = []
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('\t')
                url = parts[0]
                rating = float(parts[1])
                movie_data.append((url, rating))
        sorted_movies = sorted(movie_data, key=lambda x: x[1], reverse=not worst)
        print(f"Top 10 movies in {input_file}:" if not worst else f"Worst 10 movies in {input_file}:")
        for url, rating in sorted_movies[:10]:
            print(f"{url}\t{rating}")
        print()  # Línea en blanco para separar las listas
    except Exception as e:
        print(f'Error al procesar el archivo {input_file}: {e}')

# Función para obtener detalles de las películas desde la URL
def get_movie_details_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.text
            match = re.search(r'(.*)\s+\((\d{4})\)', title_text)
            if match:
                return match.group(1).strip(), int(match.group(2))
        return 'Unknown', 'Unknown'
    except requests.RequestException as e:
        print(f'Error al acceder a {url}: {e}')
        return 'Unknown', 'Unknown'

def main():
    url = 'https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz'
    destination = 'aclImdb_v1.tar.gz'
    download_file(url, destination)

    extract_path = 'aclImdb'
    extract_file(destination, extract_path)

    print_directory_structure(extract_path)

    neg_dir = './aclImdb/train/neg'
    pos_dir = './aclImdb/train/pos'
    neg_output_file = './aclImdb/train/neg_ratings.txt'
    pos_output_file = './aclImdb/train/pos_ratings.txt'

    extract_ratings_from_files(neg_dir, neg_output_file)
    extract_ratings_from_files(pos_dir, pos_output_file)

    urls_pos_file = './aclImdb/train/urls_pos.txt'
    urls_neg_file = './aclImdb/train/urls_neg.txt'

    pos_combined_file = './aclImdb/train/combined_pos.txt'
    neg_combined_file = './aclImdb/train/combined_neg.txt'

    combine_urls_and_ratings(urls_pos_file, pos_output_file, pos_combined_file)
    combine_urls_and_ratings(urls_neg_file, neg_output_file, neg_combined_file)

    average_pos_file = './aclImdb/train/average_pos.txt'
    average_neg_file = './aclImdb/train/average_neg.txt'

    average_ratings(pos_combined_file, average_pos_file)
    average_ratings(neg_combined_file, average_neg_file)

    print_top_10_movies(average_pos_file)
    print_top_10_movies(average_neg_file, worst=True)

if __name__ == "__main__":
    main()
