import os
import tarfile

def extract_file(tar_path, extract_path):
    if not os.path.exists(extract_path):
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall(path=extract_path)
        print(f"Archivo descomprimido en: {extract_path}")
    else:
        print(f"El directorio ya existe: {extract_path}")