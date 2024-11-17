import yaml
from utils import sonarr
from utils.youtube import download_series


# Leer la configuración desde el archivo config.yaml
def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)


def main():
    config = load_config()
    series_list = config["series"]

    for series in series_list:
        series_title = series["title"]
        playlists = series["playlist"]  # Puede ser una lista o una URL
        subtitles_language = series.get("subtitles_language")
        audio_language = series.get("audio_language")
        print(f"Procesando serie: {series_title}")

        # Verificar si 'playlist' es una lista de URLs o una sola URL
        if isinstance(playlists, list):
            # Si es una lista, procesar todas las URLs
            for playlist_url in playlists:
                print(f"Descargando desde: {playlist_url}")
                download_series(playlist_url, subtitles_language, audio_language, config, series_title)
        else:
            # Si es una sola URL, procesarla directamente
            print(f"Descargando desde: {playlists}")
            download_series(playlists, subtitles_language, audio_language, config, series_title)


if __name__ == "__main__":
    main()
