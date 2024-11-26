import logging
import shutil

logger = logging.getLogger(__name__)


def validate_series_yaml(serie):
    is_valid = True  # Iniciamos con la suposición de que es válido
    # Verificar que el formato del archivo es una lista

    # Validar que cada serie tenga un 'title' y que sea un string
    if "title" not in serie or not isinstance(serie["title"], str):
        logger.error(f"Falta 'title' o no es una cadena en la serie: {serie}")
        is_valid = False

    # Validar que 'playlist' sea una lista de URLs
    if "playlist" not in serie or not isinstance(serie["playlist"], list):
        logger.error(f"Falta 'playlist' o no es una lista en la serie: {serie}")
        is_valid = False

    for url in serie["playlist"]:
        if not isinstance(url, str) or not url.startswith("https://www.youtube.com/"):
            logger.error(f"Error: La URL de la playlist de {serie['title']} no es válida.")
            is_valid = False

    # Validar que, si existen, 'subtitles_language' y 'audio_language' sean cadenas
    if "subtitles_language" in serie and not isinstance(serie["subtitles_language"], str):
        logger.error(f"'subtitles_language' debe ser una cadena en la serie: {serie}")
        is_valid = False

    if "audio_language" in serie and not isinstance(serie["audio_language"], str):
        logger.error(f"'audio_language' debe ser una cadena en la serie: {serie}")
        is_valid = False

    if is_valid:
        logger.info("El archivo YAML está correctamente configurado.")
    else:
        logger.error("El archivo YAML tiene errores. Modifíquelo antes de continuar")
    shutil.copy("config/series.yaml", "data/series.yaml")
    return is_valid  # Devuelve True si es válido, False si tiene errores
