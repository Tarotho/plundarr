import base64
import logging
import os
import threading
import time

from flask import Flask, request, jsonify

from managers.saveManager import read_conf, delete_episode_from_downloaded
from utils.configuration.generateConfig import generate_wished_series, remove_series_by_title

logger = logging.getLogger(__name__)
app = Flask('WebhookConnector')


@app.route('/api', methods=['POST'])
def webhook():
    config = read_conf()

    youtube_tag = config.get('sonarr', 'youtube_tag', fallback=None)
    # Verificar el encabezado de autorización
    auth_header = request.headers.get('Authorization')
    if not auth_header or not verify_auth(auth_header, config):
        return jsonify({"error": "Unauthorized"}), 401

    # Procesar el cuerpo del webhook
    data = request.json
    event_type = data.get("eventType")
    series_data = data.get("series")
    if event_type == "Test":
        logger.info('la conexion con sonarr es correcta')
        return jsonify({"status": "received"}), 200
    elif event_type == "SeriesAdd":
        generate_wished_series(youtube_tag)
        logger.info(f"Serie actualizada: {series_data['title']}")
        return jsonify({"status": "received"}), 200
    elif event_type == "SeriesDelete":
        remove_series_by_title(data["series"]['title'])
        logger.info(f"Serie eliminada de seguimiento: {series_data['title']}")
        return jsonify({"status": "received"}), 200
    elif event_type == "EpisodeFileDelete":
        delete_episode_from_downloaded(data["series"]['title'])
        logger.info(f"episodio eliminada de descargados: {series_data['title']}")
        return jsonify({"status": "received"}), 200
    else:
        logger.error(f'No se tiene accion para el evento: {event_type}')
        return jsonify({"status": "received"}), 200


def verify_auth(auth_header, config):
    username = config['webhook']['webhook_name']
    password = config['webhook']['webhook_password']
    if not auth_header.startswith("Basic "):
        return False

    encoded_credentials = auth_header.split(" ", 1)[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
    received_username, received_password = decoded_credentials.split(":", 1)

    # Comparar las credenciales con las configuradas
    return username == received_username and password == received_password


def start_api_service():
    app.run(host="0.0.0.0", port=3737, debug=False, use_reloader=False)


def initialize_api_service():
    config_path = 'config/plundarr.conf'
    while not os.path.exists(config_path):
        print('se localiza config')
        time.sleep(1)
    webhook_thread = threading.Thread(target=start_api_service)
    webhook_thread.daemon = True  # Esto asegura que el hilo se cierre cuando el programa principal termine
    webhook_thread.start()
