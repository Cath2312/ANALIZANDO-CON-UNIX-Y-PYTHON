import pandas as pd

def average_ratings(input_file, output_file):
    try:
        df = pd.read_csv(input_file, sep='\t', header=None, names=['url', 'rating'])
        df['rating'] = df['rating'].astype(float)
        avg_df = df.groupby('url').agg({'rating': 'mean'}).reset_index()
        avg_df.to_csv(output_file, index=False, sep='\t', header=False)
        print(f'Calificaciones promedio guardadas en {output_file}')
    except Exception as e:
        print(f'Error al procesar el archivo: {e}')