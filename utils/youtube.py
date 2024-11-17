import subprocess
import yt_dlp

from utils import sonarr
from utils.save import load_downloaded_episodes, save_downloaded_episodes


def download_series(playlist_url, subtitles_language, audio_language, config, series_title):
    # Cargar los episodios ya descargados desde save.json
    downloaded_episodes = load_downloaded_episodes()

    # Usar yt-dlp para obtener la información de la lista de reproducción sin descargar
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Extraer solo la lista de videos sin descargar
    }

    downloaded = []  # Lista para almacenar los episodios descargados y sus rutas

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        for entry in playlist_info.get("entries", []):
            video_url = entry['url']
            title = entry['title']

            episode_path = sonarr.find_path_by_title(series_title, config)
            print(f"la ruta de sonarr para este episodio es {episode_path}/{title}")

            # Verificar si ya se descargó este video
            if title in downloaded_episodes:
                print(f"Ya descargado: {title}")
                continue

            print(f"Descargando: {title}")
            output_path = f"./{episode_path}/{title}.mkv"

            # Descargar el episodio
            if download_episode(video_url, output_path, subtitles_language, audio_language):
                # Si la descarga fue exitosa, agregar el episodio a la lista
                downloaded.append((output_path, title))
                downloaded_episodes.append(title)

                # Guardar la lista actualizada de episodios descargados
                save_downloaded_episodes(downloaded_episodes)

    return downloaded


def download_episode(video_url, output_path, subtitles_language, audio_language):
    command = generate_command(subtitles_language, audio_language)
    command += ["-o", output_path, video_url]

    try:
        print(f"El comando a usar es: {command}")
        subprocess.run(command, check=True)
        print(f"Descarga completada")
        return True  # Indicar que la descarga fue exitosa
    except subprocess.CalledProcessError as e:
        print(f"Error al descargar el video: {e}")
        return False  # Indicar que la descarga falló


def generate_command(subtitles_language, audio_language):
    command = ["yt-dlp", "-f"]
    if audio_language:
        command += [f"bv+{'+'.join([f'ba[language={lang}]' for lang in audio_language.split(',')])}",
                    "--audio-multistreams"]
    else:
        command += ["bv+ba"]

    if subtitles_language:
        command += ["--sub-langs",
                    ','.join([f"{lang}.*" for lang in subtitles_language.split(',')]),
                    "--embed-subs"]

    # Definir el comando de yt-dlp
    command += ["--embed-metadata",
                "--merge-output-format", "mkv"]
    return command
