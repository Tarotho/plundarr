import logging
import os
import shutil

from connectors.sonarr import Sonarr
from utils.save import save_conf

logger = logging.getLogger(__name__)


def validate_series_yaml(data):
    is_valid = True  # Iniciamos con la suposición de que es válido
    # Verificar que el formato del archivo es una lista
    if not isinstance(data, list):
        logger.error("El archivo YAML debe ser una lista de series.")
        is_valid = False  # Si no es una lista, marcamos como no válido

    for series in data:
        if not isinstance(series, dict):
            logger.error(f"Cada entrada debe ser un diccionario, pero se encontró: {type(series)}")
            is_valid = False

        # Validar que cada serie tenga un 'title' y que sea un string
        if "title" not in series or not isinstance(series["title"], str):
            logger.error(f"Falta 'title' o no es una cadena en la serie: {series}")
            is_valid = False

        # Validar que 'playlist' sea una lista de URLs
        if "playlist" not in series or not isinstance(series["playlist"], list):
            logger.error(f"Falta 'playlist' o no es una lista en la serie: {series}")
            is_valid = False

        for url in series["playlist"]:
            if not isinstance(url, str) or not url.startswith("https://www.youtube.com/"):
                logger.error(f"Error: La URL de la playlist no es válida: {url}")
                is_valid = False

        # Validar que, si existen, 'subtitles_language' y 'audio_language' sean cadenas
        if "subtitles_language" in series and not isinstance(series["subtitles_language"], str):
            logger.error(f"'subtitles_language' debe ser una cadena en la serie: {series}")
            is_valid = False

        if "audio_language" in series and not isinstance(series["audio_language"], str):
            logger.error(f"'audio_language' debe ser una cadena en la serie: {series}")
            is_valid = False

    if is_valid:
        logger.info("El archivo YAML está correctamente configurado.")
    else:
        logger.error("El archivo YAML tiene errores. Modifíquelo antes de continuar")
    shutil.copy("config/series.yaml", "data/series.yaml")
    return is_valid  # Devuelve True si es válido, False si tiene errores


def generate_conf():
    generate_sonarr_configuration()
    generate_telegram_configuration()
    save_youtube_tag_id()


def generate_telegram_configuration():
    config = {
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
    }
    save_conf(config, 'telegram')
    logger.debug(config)
    return config


def generate_sonarr_configuration():
    config = {
        'api_ip': os.getenv('SONARR_API_IP', ''),
        'api_port': os.getenv('SONARR_API_PORT', ''),
        'api_key': os.getenv('SONARR_API_KEY', '')
    }
    save_conf(config, 'sonarr')

    logger.debug(config)

    return config


# Función para buscar el ID del tag llamado "YouTube"
def save_youtube_tag_id():
    sonarr = Sonarr()

    tags = sonarr.get_tags()
    for tag in tags:
        if tag["label"].lower() == "youtube":
            config = {
                'sonarr_youtube_tag': tag['id']
            }
            save_conf(config, 'sonarr')
    return None
