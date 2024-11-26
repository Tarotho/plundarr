import base64
import os
import threading

from flask import Flask, request, jsonify

from utils.configuration.configuration import generate_wished_series
from utils.save import read_conf

app = Flask(__name__)


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
    print(f'recibido webhook {data}')
    event_type = data.get("eventType")
    # Los 'eventType':
    #
    # 'SeriesAdd'
    # 'SeriesDelete'
    # 'Test'
    # 'EpisodeFileDelete'
    if event_type == "Series Added" or "Metadata":
        generate_wished_series(youtube_tag)
        series_data = data.get("series")
        print(f"Serie actualizada: {series_data['title']}")
        # Aquí puedes hacer lo que necesites con la información
        # Por ejemplo, actualizar una base de datos, registrar el cambio, etc.

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
    app.run(host="192.168.0.2", port=5000, debug=False, use_reloader=False)


def initialize_api_service():
    config_path = 'config/plundarr.conf'
    while not os.path.exists(config_path):
        webhook_thread = threading.Thread(target=start_api_service)
        webhook_thread.daemon = True  # Esto asegura que el hilo se cierre cuando el programa principal termine
        webhook_thread.start()
