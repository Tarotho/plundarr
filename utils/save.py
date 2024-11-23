import json


# Leer los episodios descargados desde save.json
def load_downloaded_episodes():
    try:
        with open("data/save.json", "r") as file:
            data = json.load(file)
            return data.get("downloads", [])
    except FileNotFoundError:
        # Si el archivo no existe, devolvemos una lista vacía
        return []


# Guardar los episodios descargados en save.json
def save_downloaded_episodes(episodes):
    with open("data/save.json", "w") as file:
        json.dump({"downloads": episodes}, file, indent=4)


def is_episode_downloaded(title_video, downloaded_episodes):
    return title_video in downloaded_episodes
