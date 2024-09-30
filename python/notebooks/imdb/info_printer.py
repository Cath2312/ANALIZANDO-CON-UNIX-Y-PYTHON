import os
import stat
import datetime

def print_file_info(file_path):
    try:
        file_stat = os.stat(file_path)
        size = file_stat.st_size
        if size < 1024:
            size_rep = f'{size} bytes'
        elif size < 1048576:
            size_rep = f'{size / 1024:.2f} KiB'
        elif size < 1073741824:
            size_rep = f'{size / 1048576:.2f} MiB'
        else:
            size_rep = f'{size / 1073741824:.2f} GiB'

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