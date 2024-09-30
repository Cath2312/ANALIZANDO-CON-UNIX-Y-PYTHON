import os

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