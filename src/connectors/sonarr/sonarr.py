import logging

import requests

from managers.saveManager import read_conf

logger = logging.getLogger('SonarrConnector')


class Sonarr:

    def __init__(self):
        config_parser = read_conf()
        sonarr_config = config_parser['sonarr']

        api_ip = sonarr_config.get("api_ip")
        api_port = sonarr_config.get("api_port")
        api_key = sonarr_config.get("api_key")

        # Construir la URL base de la API de Sonarr
        self.base_url = f"http://{api_ip}:{api_port}"
        self.headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Content-Type': 'application/json',
                        "X-Api-Key": api_key}

    def get_series(self):
        logger.info('se intenta capturar la informacion de las series de Sonarr')
        url = f"{self.base_url}/api/v3/series"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            logger.info('La informacion se captura correctamente')
            return response.json()
        else:
            logger.error('hay un error al capturar las series')
            return f"Error al obtener las series: {response.status_code}"

    def get_episodes_from_series_id(self, series_id):
        url = f"{self.base_url}/api/v3/episode"
        params = {"seriesId": series_id}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al comunicarse con la API de Sonarr: {e}")
            return []
        except KeyError as e:
            logger.error(f"Error al procesar la respuesta de la API: {e}")
            return []

    def get_episodes(self, folder):
        url = f"{self.base_url}/api/v3/manualimport?folder={folder}"

        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def import_episodes(self, episode_list):
        base_url = f"{self.base_url}/api/v3/command"
        if not episode_list:  # Si el JSON está vacío o None
            raise RuntimeError("Error: La carpeta está vacía, no hay nada que importar.")
        for episode in episode_list:
            try:
                r = requests.post(base_url, headers=self.headers, json=episode)
                r.raise_for_status()
                logger.info(f"episodio importado correctametne por sonarr")
            except Exception as err:  # Captura cualquier excepción
                logger.error(f"Ha ocurrido un error mientras se importaba {episode['files']['path']}: {err}")
                # Opcional: podrías relanzar una excepción genérica si lo prefieres
                raise RuntimeError("Ha ocurrido un error durante el proceso de importación.")

    def get_tags(self):
        url = f"{self.base_url}/api/v3/tag"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
