import logging
import os
import time

from managers.saveManager import load_series_list
from managers.seriesManager import download_series
from threadStarted.threadStarted import initialize_api_service, initialize_watcher
from utils.configuration.generateConfig import generate_conf
from utils.configuration.validateConfig import validate_series_yaml

logger = logging.getLogger('Main')


def main():
    wished_series_list = load_series_list()
    for wished_series in wished_series_list:
        if validate_series_yaml(wished_series):
            download_series(wished_series)


if __name__ == "__main__":
    generate_conf()
    initialize_api_service()
    initialize_watcher()
    while True:
        main()
        download_interval = os.getenv('DOWNLOAD_INTERVAL', '60')
        logger.info(f"Esperando {download_interval} minutos antes de la siguiente ejecución...")
        time.sleep(int(download_interval) * 60)  # Dormir por el intervalo (convertido a segundos)
