import logging
import os
from os.path import exists

import yaml

from connectors.sonarr.sonarr import Sonarr
from managers.saveManager import read_conf, save_conf
from managers.seriesManager import filter_series_by_tag

logger = logging.getLogger('ConfigGenerator')


def generate_conf():
    logger.info('Se inicia proceso de generacion de archivos de configuración')
    generate_sonarr_configuration()
    generate_telegram_configuration()
    save_youtube_tag_id()
    generate_webhook_configuration()
    youtube_tag = read_conf().get('sonarr', 'youtube_tag', fallback=None)
    generate_wished_series(youtube_tag)
    generate_save_file()


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

    if exists(yaml_file):
        logger.info(f'el archivo {yaml_file} ya existe, procedemos a actualizarlo')
        with open(yaml_file, "r") as file:
            data = yaml.safe_load(file) or {"series": []}
    else:
        logger.info(f'el archivo {yaml_file} no existe, creamos uno nuevo vacío')
        data = {"series": []}

    existing_titles = {serie["title"] for serie in data["series"]}

    data["series"] = [serie for serie in data["series"] if serie["title"] in whished_series]

    for serie in whished_series:
        if serie not in existing_titles:
            new_entry = {
                "title": serie,
                "playlist": [""],
                "subtitles_language": "",
                "audio_language": ""
            }
            data["series"].append(new_entry)

    with open(yaml_file, "w") as file:
        yaml.safe_dump(data, file, sort_keys=False)

    return data


def remove_series_by_title(title, yaml_file="config/series.yaml"):
    if exists(yaml_file):
        with open(yaml_file, "r") as file:
            data = yaml.safe_load(file) or {"series": []}
    else:
        logger.info(f'El archivo {yaml_file} no existe, no hay series para eliminar.')
        return None

    series_to_keep = [serie for serie in data["series"] if serie["title"] != title]

    if len(series_to_keep) == len(data["series"]):
        logger.info(f'No se encontró ninguna serie con el título "{title}" en el archivo.')
    else:
        data["series"] = series_to_keep
        logger.info(f'Se ha eliminado la serie con el título "{title}".')

    with open(yaml_file, "w") as file:
        yaml.safe_dump(data, file, sort_keys=False)

    return data


def generate_telegram_configuration():
    config = {
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
    }
    save_conf(config, 'telegram')

    return config
