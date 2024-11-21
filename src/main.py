import yaml

from src.connectors.telegram import activate_telegram
from src.managers.episodeManager import generate_episode_information
from src.utils.save import load_downloaded_episodes, is_episode_downloaded
from src.managers.seriesManager import download_video
from src.connectors.youtube import get_playlist_info


# Leer la configuración desde el archivo config.yaml
def load_config():
    with open("src/data/config.yaml", "r") as file:
        return yaml.safe_load(file)


def main():
    config = load_config()
    downloaded_episodes = load_downloaded_episodes()  # Cargar los episodios ya descargados desde save.json

    wished_series_list = config["series"]

    for wished_series in wished_series_list:
        playlists = wished_series["playlist"]  # Puede ser una lista o una URL

        for playlist_url in playlists:  # Descargamos cada una de las playlist usando su url

            playlist_info = get_playlist_info(playlist_url)  # Obtener la información de la lista de reproducción

            for video_information in playlist_info.get("entries"):
                title_video = video_information['title']
                if is_episode_downloaded(title_video, downloaded_episodes):  # Verificar si ya se descargó este video
                    print(f"El capitulo {title_video} ya fué descargado con anterioridad, saltando.")
                    continue
                print(f'Se procede a descargar {title_video}')
                episode_information = generate_episode_information(video_information, wished_series)
                telegram = activate_telegram(config.get('telegram'))
                download_video(episode_information, downloaded_episodes, telegram)


if __name__ == "__main__":
    main()
