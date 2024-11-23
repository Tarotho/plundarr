def validate_series_yaml(data):
    # Verificar que el formato del archivo es una lista
    if not isinstance(data, list):
        raise ValueError("El archivo YAML debe ser una lista de series.")

    for series in data:
        if not isinstance(series, dict):
            raise ValueError(f"Cada entrada debe ser un diccionario: {type(series)}")

        # Validar que cada serie tenga un 'title' y que sea un string
        if "title" not in series or not isinstance(series["title"], str):
            raise ValueError(f"Falta 'title' o no es una cadena en la serie: {series}")

        # Validar que 'playlist' sea una lista de URLs
        if "playlist" not in series or not isinstance(series["playlist"], list):
            raise ValueError(f"Falta 'playlist' o no es una lista en la serie: {series}")

        for url in series["playlist"]:
            if not isinstance(url, str) or not url.startswith("https://www.youtube.com/"):
                raise ValueError(f"La URL de la playlist no es válida: {url}")

        # Validar que, si existen, 'subtitles_language' y 'audio_language' sean cadenas
        if "subtitles_language" in series and not isinstance(series["subtitles_language"], str):
            raise ValueError(f"'subtitles_language' debe ser una cadena: {series}")

        if "audio_language" in series and not isinstance(series["audio_language"], str):
            raise ValueError(f"'audio_language' debe ser una cadena: {series}")

    print("El archivo YAML está correctamente configurado.")
