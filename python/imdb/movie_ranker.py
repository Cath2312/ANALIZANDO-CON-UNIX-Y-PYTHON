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
        print()  # Línea en blanco para separar listas
    except Exception as e:
        print(f'Error al procesar el archivo {input_file}: {e}')