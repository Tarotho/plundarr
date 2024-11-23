import os
import re
import shutil


def sanitize_filename(filename):
    """
    Limpia un nombre de archivo eliminando caracteres no válidos para el sistema de archivos.
    :param filename: Nombre del archivo original.
    :return: Nombre del archivo limpio.
    """
    # Reemplaza caracteres problemáticos con un guion bajo
    return re.sub(r'[<>:"/\\|?*\']', '', filename)


def generate_command(episode_information):
    # Obtener las listas de idiomas de subtítulos y audio
    subtitles = episode_information.get("subtitles_language", [])
    audio_tracks = episode_information.get("audio_language", [])

    command = ["yt-dlp", "-q", "-f"]
    if audio_tracks:
        command += [f"bv[ext=mp4]+{'+'.join([f'ba[language={lang}]' for lang in audio_tracks])}",
                    "--audio-multistreams"]
    else:
        command += ["bv+ba"]

    if subtitles:
        command += ["--write-auto-subs",
                    "--sub-langs",
                    ','.join([f"{lang}" for lang in subtitles]),
                    "--embed-subs"]

    # Definir el comando de yt-dlp
    command += ["--embed-metadata",
                "--merge-output-format", "mkv"]
    command += ["-o", f".{episode_information.get('downloadsPath')}{episode_information.get('finalEpisodeTitle')}.mkv",
                episode_information['youtubeUrl']]
    return command


def move_files(episode_path, title):
    temp_path = f"./downloads/{title}.mkv"
    final_path = f".{episode_path}/{title}.mkv"

    try:
        # Crear la ruta de destino si no existe
        os.makedirs(os.path.dirname(final_path), exist_ok=True)

        # Mover el archivo
        shutil.move(temp_path, final_path)
        print(f"Archivo movido a: {final_path}")
    except Exception as e:
        print(f"Error al mover el archivo {title}: {e}")


def episode_title_reduction(episode_title, serie_title):
    # Dividir el título de la serie en palabras y crear un patrón para buscar esas palabras en el título del episodio
    pattern = r'\b(' + '|'.join(re.escape(word) for word in serie_title.split()) + r')\b'

    # Usar re.sub para reemplazar todas las coincidencias con una cadena vacía
    reduced_title = re.sub(pattern, '', episode_title, flags=re.IGNORECASE)

    # Eliminar espacios adicionales generados por la sustitución
    reduced_title = ' '.join(reduced_title.split())

    return reduced_title


def word_count_overlap(title1, title2):
    # Convertir ambos títulos a minúsculas y dividir en palabras
    words1 = set(re.findall(r'\w+', title1.lower()))
    words2 = set(re.findall(r'\w+', title2.lower()))
    # Contar las palabras comunes
    return len(words1 & words2)


def format_episode_title(episode_information):
    # Extraer información de la serie
    series_title = episode_information['seriesTitle']
    series_year = episode_information['seriesYear']
    quality = f"{episode_information['resolution']}"

    # Extraer información del episodio
    season = episode_information['seasonNumber']
    episode = episode_information['episodeNumber']
    episode_clean_title = sanitize_filename(episode_information['episodeTitle'])

    # Construir el título
    formatted_title = (
        f"{series_title} ({series_year}) - S{season:02}E{episode:02} - {episode_clean_title} "
        f"[WEB-DL {quality}p]-Youtube"
    )

    return formatted_title
