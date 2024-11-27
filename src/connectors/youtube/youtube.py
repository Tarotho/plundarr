import logging
import subprocess

import yt_dlp

logger = logging.getLogger('YdlConnector')


def get_format_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestvideo',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
    return result


def download_episode(command):
    try:
        logger.info('Iniciando proceso de descarga')
        subprocess.run(command, check=True)
        logger.info('Descarga existosa')
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al descargar el video: {e}")
        return False


def get_playlist_info(playlist_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Extraer solo la lista de videos sin descargar
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        logger.info('Extraemos la informacion de los capitulos de la playlist')
        return ydl.extract_info(playlist_url, download=False)
