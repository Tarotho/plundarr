import os

import yaml


def validate_series_yaml(data):
    is_valid = True  # Iniciamos con la suposición de que es válido
    # Verificar que el formato del archivo es una lista
    if not isinstance(data, list):
        print("Error: El archivo YAML debe ser una lista de series.")
        is_valid = False  # Si no es una lista, marcamos como no válido

    for series in data:
        if not isinstance(series, dict):
            print(f"Error: Cada entrada debe ser un diccionario, pero se encontró: {type(series)}")
            is_valid = False

        # Validar que cada serie tenga un 'title' y que sea un string
        if "title" not in series or not isinstance(series["title"], str):
            print(f"Error: Falta 'title' o no es una cadena en la serie: {series}")
            is_valid = False

        # Validar que 'playlist' sea una lista de URLs
        if "playlist" not in series or not isinstance(series["playlist"], list):
            print(f"Error: Falta 'playlist' o no es una lista en la serie: {series}")
            is_valid = False

        for url in series["playlist"]:
            if not isinstance(url, str) or not url.startswith("https://www.youtube.com/"):
                print(f"Error: La URL de la playlist no es válida: {url}")
                is_valid = False

        # Validar que, si existen, 'subtitles_language' y 'audio_language' sean cadenas
        if "subtitles_language" in series and not isinstance(series["subtitles_language"], str):
            print(f"Error: 'subtitles_language' debe ser una cadena en la serie: {series}")
            is_valid = False

        if "audio_language" in series and not isinstance(series["audio_language"], str):
            print(f"Error: 'audio_language' debe ser una cadena en la serie: {series}")
            is_valid = False

    if is_valid:
        print("El archivo YAML está correctamente configurado.")
    else:
        print("El archivo YAML tiene errores. Revísalos. Se volverá a intentar en 10 minutos")

    return is_valid  # Devuelve True si es válido, False si tiene errores


def load_and_replace_env_vars(yaml_file):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)

    # Reemplazar las variables de entorno en el archivo YAML
    for key, value in config.items():
        if isinstance(value, str):
            # Reemplazar las variables de entorno dentro de las cadenas
            config[key] = os.path.expandvars(value)
            print(f'se modifica el valor {key} por {os.path.expandvars(value)}')

    return config
