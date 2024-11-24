import json
import logging

import yaml

logger = logging.getLogger(__name__)


# Leer los episodios descargados desde save.json
def load_downloaded_episodes():
    try:
        with open("config/save.json", "r") as file:
            data = json.load(file)
            return data.get("downloads", [])
    except FileNotFoundError:
        # Si el archivo no existe, devolvemos una lista vacía
        return []


# Guardar los episodios descargados en save.json
def save_downloaded_episodes(episodes):
    logger.info('se procede a guardar la informacion de los capitulos descargados')
    with open("config/save.json", "w") as file:
        json.dump({"downloads": episodes}, file, indent=4)


def is_episode_downloaded(title_video, downloaded_episodes):
    return title_video in downloaded_episodes


def save_conf(config, section, file_path='config/plundarr.conf'):
    # Crear objeto ConfigParser
    config_parser = configparser.ConfigParser()

    # Intentar leer el archivo de configuración si ya existe
    if os.path.exists(file_path):
        config_parser.read(file_path)

    # Añadir o actualizar la sección
    if section not in config_parser.sections():
        config_parser.add_section(section)

    # Añadir las opciones de configuración en la sección correspondiente
    for key, value in config.items():
        config_parser.set(section, key, value)

    try:
        # Guardar el archivo, actualizando el contenido
        with open(file_path, 'w', encoding='utf-8') as configfile:
            config_parser.write(configfile)

        logger.info(f"Configuración guardada/actualizada en {file_path}")
    except Exception as e:
        logger.error(f"Error al guardar la configuración: {e}")


import configparser
import os


def read_conf(file_path='config/plundarr.conf'):
    # Crear objeto ConfigParser
    config_parser = configparser.ConfigParser()

    # Verificar si el archivo existe antes de intentar leerlo
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe.")
        return None

    try:
        # Leer el archivo de configuración
        config_parser.read(file_path, encoding='utf-8')

        # Verificar si se han cargado secciones
        if not config_parser.sections():
            print(f"No se encontraron secciones en el archivo {file_path}.")
            return None

        # Mostrar todas las secciones del archivo
        print("Secciones disponibles:")
        for section in config_parser.sections():
            print(f"[{section}]")
            for key, value in config_parser.items(section):
                print(f"{key} = {value}")

        # Retornar el objeto config_parser para uso posterior
        return config_parser

    except Exception as e:
        print(f"Error al leer el archivo de configuración: {e}")
        return None


def load_series_list():
    try:
        with open("config/series.yaml", "r") as file:
            series = yaml.safe_load(file)
            return series['series']
    except Exception as e:
        logging.error(f"Error al cargar el archivo de configuración: {e}")
        return None
