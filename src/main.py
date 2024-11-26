import logging
import os
import time

from connectors.telegram.telegram import activate_telegram
from connectors.webhook.webhook import initialize_api_service
from connectors.youtube.youtube import get_playlist_info
from managers.episodeManager import generate_episode_information
from managers.fileManager import validate_series_yaml
from managers.seriesManager import download_video
from utils.configuration.configuration import generate_telegram_configuration, generate_conf
from utils.save import load_downloaded_episodes, is_episode_downloaded, load_series_list

logger = logging.getLogger(__name__)


def main():
    downloaded_episodes = load_downloaded_episodes()
    wished_series_list = load_series_list()
    for wished_serie in wished_series_list:
        if validate_series_yaml(wished_serie):
            playlists = wished_serie["playlist"]

            for playlist_url in playlists:
                playlist_info = get_playlist_info(playlist_url)  # Obtener la información de la lista de reproducción

                for video_information in playlist_info.get("entries"):
                    title_video = video_information['title']
                    if is_episode_downloaded(title_video, downloaded_episodes):
                        logger.warning(f"El capitulo {title_video} ya fué descargado con anterioridad, saltando.")
                        continue
                    logger.info(f'Se procede a descargar {title_video}')
                    episode_information = generate_episode_information(video_information, wished_serie)
                    if episode_information.get('isMonitored'):
                        logger.info('Sonarr Monitoriza este episodio')
                        if not episode_information.get('hasFile'):
                            logger.info('Sonarr no posee este episodio')
                            telegram = activate_telegram(generate_telegram_configuration())
                            download_video(episode_information, downloaded_episodes, telegram)
                        else:
                            logger.info(f'Sonarr ya posee este episodio, no se descarga.')

                    else:
                        logger.info('Sonarr no Monitoriza este episodio, no se descarga.')


if __name__ == "__main__":
    generate_conf()
    initialize_api_service()
    while True:  # Ciclo infinito
        main()
        download_interval = os.getenv('DOWNLOAD_INTERVAL', '60')
        logger.info(f"Esperando {download_interval} minutos antes de la siguiente ejecución...")
        time.sleep(int(download_interval) * 60)  # Dormir por el intervalo (convertido a segundos)
