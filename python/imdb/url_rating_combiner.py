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