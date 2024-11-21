from src.managers.episodeManager import import_episode_using_sonarr
from src.utils.save import save_downloaded_episodes
from src.connectors.telegram import Telegram
from src.utils.utils import move_files
from src.connectors.youtube import download_episode


def download_video(episode_information, downloaded_episodes):
    telegram = Telegram()  # Crear una instancia de Telegram para enviar mensajes

    if download_episode(episode_information['command']):  # Descargar el episodio
        print(f"Descarga completada")
        downloaded_episodes.append(
            episode_information.get('youtubeTitle'))  # Si la descarga fue exitosa, agregar el episodio a la lista
        save_downloaded_episodes(downloaded_episodes)  # Guardar la lista actualizada de episodios descargados
        # Intentar importar automáticamente el episodio
        if import_episode_using_sonarr(episode_information.get('downloadsPath')):

            telegram.send_message(
                f"episodio {episode_information['finalEpisodeTitle']} importado por sonarr desde youtubarr")
        else:
            move_files(episode_information.get('episodePath'), episode_information['finalEpisodeTitle'])
            telegram.send_message(
                f"no se ha podido importar {episode_information['finalEpisodeTitle']}, "
                f"por favor, importalo manualmente")
