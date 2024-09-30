import os
import requests

def download_file(url, destination):
    if not os.path.exists(destination):
        response = requests.get(url, stream=True)
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Archivo descargado: {destination}")
    else:
        print(f"El archivo ya existe: {destination}")