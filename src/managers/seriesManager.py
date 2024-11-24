import logging

from connectors.sonarr.sonarr import Sonarr
from connectors.telegram.telegram import Telegram
from connectors.youtube.youtube import download_episode
from managers.episodeManager import import_episode_using_sonarr
from utils.save import save_downloaded_episodes
from utils.utils import move_files

logger = logging.getLogger(__name__)


def download_video(episode_information, downloaded_episodes, telegram):
    if telegram:
        telegram = Telegram()  # Crear una instancia de Telegram para enviar mensajes

    if download_episode(episode_information['command']):  # Descargar el episodio
        logger.info(f"Descarga completada")
        downloaded_episodes.append(
            episode_information.get('youtubeTitle'))  # Si la descarga fue exitosa, agregar el episodio a la lista
        save_downloaded_episodes(downloaded_episodes)  # Guardar la lista actualizada de episodios descargados
        # Intentar importar automáticamente el episodio
        if import_episode_using_sonarr(episode_information.get('downloadsPath')):
            if telegram:
                telegram.send_message(
                    f"episodio {episode_information['finalEpisodeTitle']} importado por sonarr desde youtubarr")
        else:
            move_files(episode_information.get('episodePath'), episode_information['finalEpisodeTitle'])
            if telegram:
                telegram.send_message(
                    f"no se ha podido importar {episode_information['finalEpisodeTitle']}, "
                    f"por favor, importalo manualmente")


# Función para filtrar las series que contienen el ID del tag
def filter_series_by_tag(tag_id):
    sonarr = Sonarr()
    series = sonarr.get_series()

    series_list = [serie['title'] for serie in series if int(tag_id) in serie.get("tags", [])]
    logger.debug(f'las series encontradas son: {series_list}')
    return series_list
