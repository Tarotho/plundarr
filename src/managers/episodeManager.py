import logging

from connectors.sonarr.sonarr import Sonarr
from connectors.telegram.telegram import Telegram
from connectors.youtube.youtube import download_episode
from managers.saveManager import save_downloaded_episodes
from utils.configuration.validateConfig import validate_telegram_configuration
from utils.utils import word_count_overlap, move_files

logger = logging.getLogger('EpisodeManager')


def download_video(episode_information, downloaded_episodes):
    is_telegram_activate = validate_telegram_configuration()
    telegram = Telegram() if is_telegram_activate else None

    if not download_episode(episode_information['command']):
        logger.error("La descarga del episodio falló")
        return

    logger.info(f'episodio descargado en {episode_information["downloadsPath"]}')

    if import_episode_using_sonarr(episode_information['downloadsPath']):
        handle_successful_download(telegram, downloaded_episodes, episode_information['episodeTitle'],
                                   success_message=True)
    elif move_files(episode_information):
        handle_successful_download(telegram, downloaded_episodes, episode_information['episodeTitle'],
                                   success_message=False)
    else:
        logger.error("No se pudo importar ni mover el episodio")


def handle_successful_download(telegram, downloaded_episodes, episode_title, success_message):
    logger.info('Se incluye el capitulo a la lista de descargados')
    downloaded_episodes.append(episode_title)
    save_downloaded_episodes(downloaded_episodes)
    if telegram:
        message = (
            f"Episodio {episode_title} importado por Sonarr desde Youtubarr"
            if success_message
            else f"No se ha podido importar {episode_title}, por favor, impórtalo manualmente"
        )
        telegram.send_message(message)


def get_episode_information(episode_title, series_id):
    sonarr = Sonarr()
    episodes_information = sonarr.get_episodes_from_series_id(series_id)
    # Inicializar variables para rastrear el episodio con más coincidencias
    max_overlap = 0
    best_match = None
    for episode in episodes_information:
        # Contar las palabras coincidentes entre el título del episodio dado y el actual
        overlap = word_count_overlap(episode_title, episode["title"])
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = episode
    return best_match


def get_episode_data(episode_information):
    episode_data = []
    logger.info("extrayendo información usando el api sonarr")
    for episode in episode_information:
        data = {
            "name": "ManualImport",
            "files": [{
                "path": episode['path'],
                "seriesId": episode['series']['id'],
                "episodeIds": [e['id'] for e in episode['episodes']],
                "releaseGroup": episode.get('releaseGroup'),
                "quality": episode.get('quality'),
                "languages": episode.get('languages'),
                "indexerFlags": episode.get('indexerFlags')
            }],
            "importMode": "move"
        }
        episode_data.append(data)
    return episode_data


def import_episode_using_sonarr(episode_path):
    sonarr = Sonarr()
    logger.info("intentando capiturar informacion del episodio")
    try:
        response = sonarr.get_episodes(episode_path)
        logger.info("Sonarr a retornado informacion adecuada")
        sonarr.import_episodes(get_episode_data(response))
        logger.info('sonarr ha importado los episodios correctamente')
        return True
    except Exception as e:
        logger.error(f"Error al importar episodio: {e}")
        return False


def should_download_video(title_video, downloaded_episodes, episode_information):
    logger.debug(downloaded_episodes)
    if title_video in downloaded_episodes:
        logger.warning(f"El capitulo {title_video} ya fué descargado con anterioridad, saltando.")
        return False
    if not episode_information.get('isMonitored'):
        logger.info('Sonarr no Monitoriza este episodio, no se descarga.')
        return False
    if episode_information.get('hasFile'):
        logger.info(f'Sonarr ya posee este episodio, no se descarga.')
        return False
    else:
        return True
