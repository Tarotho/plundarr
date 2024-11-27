import logging

from connectors.sonarr.sonarr import Sonarr
from connectors.youtube.youtube import get_playlist_info, get_format_info
from managers.episodeManager import download_video, should_download_video, get_episode_information
from managers.saveManager import load_downloaded_episodes
from utils.utils import format_episode_title, generate_command, episode_title_reduction

logger = logging.getLogger('SeriesManager')


def download_series(wished_serie):
    playlists = wished_serie["playlist"]
    for playlist_url in playlists:
        playlist_info = get_playlist_info(playlist_url)
        for video_information in playlist_info.get("entries"):
            episode_information = generate_information(video_information, wished_serie)
            title_video = episode_information['episodeTitle']
            downloaded_episodes = load_downloaded_episodes()
            if should_download_video(title_video, downloaded_episodes, episode_information):
                logger.info(f'Se procede a descargar {title_video}')
                download_video(episode_information, downloaded_episodes)


def filter_series_by_tag(tag_id):
    sonarr = Sonarr()
    series = sonarr.get_series()
    series_list = [serie['title'] for serie in series if int(tag_id) in serie.get("tags", [])]
    return series_list


def get_series_information(series_name):
    logger.info('se instancia Sonarr')
    sonarr = Sonarr()
    series_data = sonarr.get_series()
    for series in series_data:
        if series_name.lower() in series.get("title").lower():  # Comparar título exacto
            return series
    return "Serie no encontrada"


def generate_information(video_information, wished_series):
    youtube_title = video_information['title']
    wished_series_title = wished_series['title']
    youtube_url = video_information['url']
    episode_title = episode_title_reduction(youtube_title, wished_series_title)
    series_information = get_series_information(wished_series_title)
    series_id = series_information.get('id')
    episode_information = get_episode_information(episode_title, series_id)
    format_information = get_format_info(youtube_url)
    best_video = None
    for formats in format_information['formats']:
        if formats.get('height'):
            if best_video is None or best_video.get('height') < formats.get('height'):
                best_video = formats
    episode_information = {
        "youtubeTitle": youtube_title,
        "youtubeUrl": youtube_url,
        "seriesTitle": series_information.get("title"),
        "seriesId": series_id,
        "downloadsPath": "/plundarr",
        "seriesPath": series_information.get("path"),
        "episodePath": f"{series_information.get('path')}/"
                       f"Season {episode_information.get('seasonNumber'):02}",
        "seriesYear": series_information.get("year"),
        "episodeTitle": episode_information.get("title"),
        "seasonNumber": episode_information.get("seasonNumber"),
        "episodeNumber": episode_information.get("episodeNumber"),
        "isMonitored": episode_information.get('monitored'),
        "hasFile": episode_information.get('hasFile'),
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
