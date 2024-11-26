import logging
import os
import re
import shutil

# Configuración global de logging
logging.basicConfig(
    level=logging.DEBUG,  # Puedes elegir el nivel de log que necesites
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato del log
    handlers=[logging.StreamHandler()]  # Esto imprime los logs en la consola
)

logger = logging.getLogger(__name__)


def sanitize_filename(filename):
    # Reemplaza caracteres problemáticos con un espacio
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
    command += ["-o",
                f"..{episode_information.get('downloadsPath')}/{episode_information.get('finalEpisodeTitle')}.mkv",
                episode_information['youtubeUrl']]
    return command


def move_files(episode_information):
    downloads_path = episode_information['downloadsPath']
    sonarr_path = episode_information['episodePath']
    final_episode_title = episode_information['finalEpisodeTitle']
    temp_path = f"..{downloads_path}/{final_episode_title}.mkv"
    final_path = f"..{sonarr_path}/{final_episode_title}.mkv"

    try:
        # Crear la ruta de destino si no existe
        if not os.path.exists(final_path):
            logger.warning(f'{final_path} no existe, se crea')
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
        # Mover el archivo
        shutil.move(temp_path, final_path)
        logger.info(f"Archivo movido a: {final_path}")
    except Exception as e:
        logger.error(f"Error al mover el archivo {final_episode_title}: {e}")


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


def move_env_conf():
    destiny_path = "/app/config/"
    origin_path = "/app/data/"
    series = "series.yaml"
    save = "save.json"
    config = "plundar.conf"
    if not os.path.exists(f"{destiny_path}{series}"):
        logger.info(f'no se ha localizado {series}, se intenta copiar')
        shutil.copy(f"{origin_path}{series}", f"{destiny_path}{series}")
    if not os.path.exists(f"{destiny_path}{save}"):
        logger.info(f'no se ha localizado {save}, se intenta copiar')
        shutil.copy(f"{origin_path}{save}", f"{destiny_path}{save}")
    if not os.path.exists(f"{destiny_path}{config}"):
        logger.info(f'no se ha localizado {config}, se intenta copiar')
        shutil.copy(f"{origin_path}{config}", f"{destiny_path}{config}")
