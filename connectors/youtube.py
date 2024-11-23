import subprocess

import yt_dlp


def get_format_info(url):
    ydl_opts = {
        'quiet': True,
        'format': 'bestvideo',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
    return result


def download_episode(command):
    try:
        subprocess.run(command, check=True)
        return True  # Indicar que la descarga fue exitosa
    except subprocess.CalledProcessError as e:
        print(f"Error al descargar el video: {e}")
        return False  # Indicar que la descarga falló


def get_playlist_info(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Extraer solo la lista de videos sin descargar
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(playlist_url, download=False)
