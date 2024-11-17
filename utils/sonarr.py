import requests


def find_path_by_title(title, config):
    # Construir la URL de la API de Sonarr para obtener todas las series
    base_url = f"http://{config['api_ip']}:{config['api_port']}/api/v3/series"
    headers = {
        "X-Api-Key": config["api_key"]
    }

    # Hacer la solicitud a la API de Sonarr para obtener las series
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        series_data = response.json()
        # Iterar sobre las series y buscar la que coincida con el título proporcionado
        for series in series_data:
            if title.lower() in series.get("title").lower():  # Comparar título exacto
                series_path = series.get("path", "Ruta no encontrada")
                return series_path

        # Si no se encuentra ninguna serie con el título dado
        return "Serie no encontrada"
    else:
        return f"Error al obtener las series: {response.status_code}"


# Ejemplo de uso
config = {
    "api_ip": "192.168.0.99",
    "api_port": 8989,
    "api_key": "tu_api_key"
}

title = "The Amazing Digital Circus"
episode_path = find_path_by_title(title, config)
print(episode_path)
