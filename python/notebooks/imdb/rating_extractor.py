import os

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