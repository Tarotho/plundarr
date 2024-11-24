import logging

from connectors.sonarr import Sonarr
from connectors.youtube import get_format_info
from utils.utils import episode_title_reduction, sanitize_filename, format_episode_title, generate_command, \
    word_count_overlap

logger = logging.getLogger(__name__)


def generate_episode_information(video_information, wished_series):
    episode_title = episode_title_reduction(sanitize_filename(video_information['title']),
                                            wished_series['title'])  # limpia el titulo del capitulo
    sonarr_series_information = get_series_information(wished_series['title'])
    sonarr_episodes_information = get_episode_information_from_sonarr(episode_title,
                                                                      sonarr_series_information.get('id'))

    # Buscamos metadatos usando yld
    format_information = get_format_info(video_information['url'])
    best_video = None
    for formats in format_information['formats']:
        if formats.get('height'):
            if best_video is None or best_video.get('height') < formats.get('height'):
                best_video = formats
    episode_information = {
        "youtubeTitle": video_information['title'],
        "youtubeUrl": video_information['url'],
        "seriesTitle": sonarr_series_information.get("title"),
        "downloadsPath": "/downloads/plundarr/",
        "seriesPath": sonarr_series_information.get("path"),
        "episodePath": f"{sonarr_series_information.get('path')}/"
                       f"Season {sonarr_episodes_information.get('seasonNumber'):02}",
        "seriesYear": sonarr_series_information.get("year"),
        "episodeTitle": sonarr_episodes_information.get("title"),
        "seasonNumber": sonarr_episodes_information.get("seasonNumber"),
        "episodeNumber": sonarr_episodes_information.get("episodeNumber"),
        "resolution": best_video.get('height'),
        "subtitles_language": wished_series.get("subtitles_language", "").split(",") if wished_series.get(
            "subtitles_language") else [],
        "audio_language": wished_series.get("audio_language", "").split(",") if wished_series.get(
            "audio_language") else [],
    }
    final_episode_title = format_episode_title(episode_information)
    episode_information.update({
        "finalEpisodeTitle": final_episode_title,
    })
    command = generate_command(episode_information)
    episode_information.update({
        "command": command
    })
    return episode_information


def get_episode_information_from_sonarr(episode_title, series_id):
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


def get_series_information(series_name):
    logger.info('se instancia Sonarr')
    sonarr = Sonarr()
    series_data = sonarr.get_series()
    # Iterar sobre las series y buscar la que coincida con el título proporcionado
    for series in series_data:
        if series_name.lower() in series.get("title").lower():  # Comparar título exacto
            return series
            # Si no se encuentra ninguna serie con el título dado
    return "Serie no encontrada"
