import requests
import yaml


def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


class Sonarr:

    def __init__(self, config_path="src/data/config.yaml"):
        config = load_config(config_path)

        api_ip = config["sonarr"]["api_ip"]
        api_port = config["sonarr"]["api_port"]
        api_key = config["sonarr"]["api_key"]

        # Construir la URL base de la API de Sonarr
        self.base_url = f"http://{api_ip}:{api_port}"
        self.headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Content-Type': 'application/json',
                        "X-Api-Key": api_key}

    def get_series(self):
        url = f"{self.base_url}/api/v3/series"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error al obtener las series: {response.status_code}"

    def get_episodes_from_series_id(self, series_id):
        url = f"{self.base_url}/api/v3/episode"
        params = {"seriesId": series_id}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al comunicarse con la API de Sonarr: {e}")
            return []
        except KeyError as e:
            print(f"Error al procesar la respuesta de la API: {e}")
            return []

    def get_episodes(self, folder):
        url = f"{self.base_url}/api/v3/manualimport?folder={folder}"

        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def import_episodes(self, episode_list):
        base_url = f"{self.base_url}/api/v3/command"
        if not episode_list:  # Si el JSON está vacío o None
            raise ValueError("Error: La carpeta está vacía, no hay nada que importar.")

        for episode in episode_list:
            try:
                r = requests.post(base_url, headers=self.headers, json=episode)
                r.raise_for_status()
                print(f"episodio importado correctametne por sonarr")
            except Exception as err:  # Captura cualquier excepción
                print(f"An error occurred while importing {episode['files']['path']}: {err}")
                # Opcional: podrías relanzar una excepción genérica si lo prefieres
                raise RuntimeError("An error occurred during the import process.")
