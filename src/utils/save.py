import configparser
import logging
import os

import yaml

logger = logging.getLogger(__name__)


def load_downloaded_episodes(file_path='config/downloaded.txt'):
    """Cargar los episodios descargados desde el archivo TXT."""
    if not os.path.exists(file_path):
        # Si el archivo no existe, devolvemos una lista vacía
        return []

    with open(file_path, 'r', encoding='utf-8') as file:
        # Leemos cada línea y la limpiamos de saltos de línea
        return [line.strip() for line in file.readlines()]


def save_downloaded_episodes(episodes, file_path='config/downloaded.txt'):
    logger.info('Se procede a guardar la información de los capítulos descargados')
    with open(file_path, 'a', encoding='utf-8') as file:
        # Escribimos cada episodio en una nueva línea
        for episode in episodes:
            file.write(f"{episode}\n")


def delete_episode_from_downloaded(title, file_path='config/downloaded.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        downloaded_episodes = [line.strip() for line in file.readlines()]

    if title not in downloaded_episodes:
        logger.info(f"El título '{title}' no se encontró en la lista de episodios descargados.")
        return False

    downloaded_episodes.remove(title)

    with open(file_path, 'w', encoding='utf-8') as file:
        for episode in downloaded_episodes:
            file.write(f"{episode}\n")

    logger.info(f"El título '{title}' ha sido eliminado de la lista de episodios descargados.")
    return True


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


def read_conf(file_path='config/plundarr.conf'):
    # Crear objeto ConfigParser
    config_parser = configparser.ConfigParser()

    # Verificar si el archivo existe antes de intentar leerlo
    if not os.path.exists(file_path):
        logger.warning(f"El archivo {file_path} no existe.")
        return None

    try:
        # Leer el archivo de configuración
        config_parser.read(file_path, encoding='utf-8')

        # Verificar si se han cargado secciones
        if not config_parser.sections():
            logger.warning(f"No se encontraron secciones en el archivo {file_path}.")
            return None

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
