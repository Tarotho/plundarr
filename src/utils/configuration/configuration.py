import logging
import os
from os.path import exists

import yaml

from connectors.sonarr.sonarr import Sonarr
from managers.seriesManager import filter_series_by_tag
from utils.save import read_conf, save_conf

logger = logging.getLogger(__name__)


def generate_conf():
    generate_sonarr_configuration()
    generate_telegram_configuration()
    save_youtube_tag_id()
    youtube_tag = read_conf().get('sonarr', 'youtube_tag', fallback=None)
    generate_wished_series(youtube_tag)
    generate_save_file()


def generate_telegram_configuration():
    config = {
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
    }
    save_conf(config, 'telegram')
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


def save_youtube_tag_id():
    sonarr = Sonarr()

    tags = sonarr.get_tags()
    for tag in tags:
        if tag["label"].lower() == "youtube":
            config = {
                'youtube_tag': str(tag['id'])
            }
            save_conf(config, 'sonarr')
    return None


def generate_save_file(txt_file="config/downloaded.txt"):
    """Comprueba si el fichero existe; si no, lo crea vacío."""
    if not exists(txt_file):
        with open(txt_file, 'w', encoding='utf-8'):
            # Crear archivo vacío
            pass
        print(f"Archivo creado: {txt_file}")
    else:
        print(f"El archivo ya existe: {txt_file}")


def generate_wished_series(tag_id, yaml_file="config/series.yaml"):
    whished_series = filter_series_by_tag(tag_id)

    # Leer contenido existente del archivo YAML (si existe)
    if exists(yaml_file):
        with open(yaml_file, "r") as file:
            data = yaml.safe_load(file) or {"series": []}
    else:
        data = {"series": []}

    # Obtener títulos existentes para evitar duplicados
    existing_titles = {serie["title"] for serie in data["series"]}

    # Crear nuevas entradas para las series que no están en el archivo
    for serie in whished_series:
        if serie not in existing_titles:
            new_entry = {
                "title": serie,
                "playlist": [""],  # Añadir la URL adecuada si se dispone
                "subtitles_language": "",
                "audio_language": ""
            }
            data["series"].append(new_entry)

    # Guardar los datos actualizados en el archivo YAML
    with open(yaml_file, "w") as file:
        yaml.safe_dump(data, file, sort_keys=False)

    return data
