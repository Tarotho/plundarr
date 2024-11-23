import shutil
import time

import yaml

from connectors.telegram import activate_telegram
from connectors.youtube import get_playlist_info
from managers.episodeManager import generate_episode_information
from managers.fileManager import validate_series_yaml, generate_config_file
from managers.seriesManager import download_video
from utils.save import load_downloaded_episodes, is_episode_downloaded


def load_series_list():
    try:
        with open("config/series.yaml", "r") as file:
            series = yaml.safe_load(file)
            return series['series']
    except Exception as e:
        print(f"Error al cargar el archivo de configuración: {e}")
        return None


def main(config):
    downloaded_episodes = load_downloaded_episodes()  # Cargar los episodios ya descargados desde save.json

    wished_series_list = load_series_list()
    if validate_series_yaml(wished_series_list):
        for wished_series in wished_series_list:
            playlists = wished_series["playlist"]  # Puede ser una lista o una URL

            for playlist_url in playlists:  # Descargamos cada una de las playlist usando su url

                playlist_info = get_playlist_info(playlist_url)  # Obtener la información de la lista de reproducción

                for video_information in playlist_info.get("entries"):
                    title_video = video_information['title']
                    if is_episode_downloaded(title_video,
                                             downloaded_episodes):  # Verificar si ya se descargó este video
                        print(f"El capitulo {title_video} ya fué descargado con anterioridad, saltando.")
                        continue
                    print(f'Se procede a descargar {title_video}')
                    episode_information = generate_episode_information(video_information, wished_series)
                    telegram = activate_telegram(config.get('telegram'))
                    download_video(episode_information, downloaded_episodes, telegram)


if __name__ == "__main__":
    shutil.move("data/series.yaml", "config/series.yaml")
    config_file = generate_config_file()  # Vuelve a cargar la configuración en cada ciclo
    while True:  # Ciclo infinito
        main(config_file)
        download_interval = int(config_file.get("download_interval", 60))
        print(f"Esperando {download_interval} minutos antes de la siguiente ejecución...")
        time.sleep(download_interval * 60)  # Dormir por el intervalo (convertido a segundos)
