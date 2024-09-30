## Estructura del Proyecto

Este proyecto está diseñado para comparar la filosofía de UNIX y la programación en Python a través del análisis de la base de datos de IMDb, obteniendo las 10 mejores y peores películas. La estructura del proyecto es la siguiente:

top-imdb/
├── cmd/
│   ├── [archivos de comandos de UNIX]
├── python/
│   ├── imdb/
│   │   ├── [módulos de Python]
│   ├── scripts/
│   │   ├── [scripts de Python]
│   ├── notebooks/
│   │   ├── [libretas Jupyter]
├── comparación.pdf
├── LEEME.md


## Requisitos Previos

- Docker
- Poetry (para gestión de dependencias en Python)
- Acceso a internet (para descargar la base de datos de IMDb)

## Instrucciones para Ejecutar Análisis

### Análisis con Línea de Comandos (en el directorio `cmd`)

1. Abre el terminal (CMD o PowerShell).
2. Navega hasta el directorio `cmd`:

   cd ..\top-imdb\cmd

3. Ejecuta el script:

   bash script_cmd.sh

###  Análisis con Python (en el directorio python)
1. Navega al directorio python:

    cd top-imdb/python

2. Instala las dependencias con Poetry:

    poetry install

3. Ejecuta los scripts de Python:

    Utiliza Poetry para ejecutar los scripts de análisis:

    poetry run python scripts/[nombre_del_script.py]

4. Ejemplo de uso en Notebooks:

    Abre Jupyter Notebook para explorar cómo utilizar la solución.

        poetry run jupyter notebook notebooks/

### Documentación
La documentación completa sobre las ventajas y desventajas de cada perspectiva se encuentra en el archivo comparación.pdf.

### Notas
Asegúrate de seguir las instrucciones para configurar adecuadamente Docker y cualquier otro requerimiento necesario para ejecutar los scripts.


