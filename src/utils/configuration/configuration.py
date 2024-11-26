import logging
import os
from os.path import exists

import yaml

from connectors.sonarr.sonarr import Sonarr
from managers.seriesManager import filter_series_by_tag
from utils.save import read_conf, save_conf

logger = logging.getLogger(__name__)


def generate_conf():
    logger.info('Se inicia proceso de generacion de archivos de configuración')
    generate_sonarr_configuration()
    generate_telegram_configuration()
    save_youtube_tag_id()
    generate_webhook_configuration()
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


def generate_webhook_configuration():
    config = {
        'webhook_name': os.getenv('PLUNDARR_USER', ''),
        'webhook_password': os.getenv('PLUNDARR_KEY', ''),
    }
    save_conf(config, 'webhook')


def generate_save_file(txt_file="config/downloaded.txt"):
    if not exists(txt_file):
        logger.info(f'no existe {txt_file}, se procede a su creación')
        with open(txt_file, 'w', encoding='utf-8'):
            pass
    else:
        logger.info(f"El archivo ya existe: {txt_file}")


def generate_wished_series(tag_id, yaml_file="config/series.yaml"):
    whished_series = filter_series_by_tag(tag_id)

    # Leer contenido existente del archivo YAML (si existe)
    if exists(yaml_file):
        logger.info(f'el archivo {yaml_file} ya existe, procedemos a actualizarlo')
        with open(yaml_file, "r") as file:
            data = yaml.safe_load(file) or {"series": []}
    else:
        logger.info(f'el archivo {yaml_file} no existe, creamos uno nuevo vacío')
        data = {"series": []}

    # Obtener títulos existentes para evitar duplicados
    existing_titles = {serie["title"] for serie in data["series"]}

    # Eliminar las series que ya no están en whished_series
    data["series"] = [serie for serie in data["series"] if serie["title"] in whished_series]

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
