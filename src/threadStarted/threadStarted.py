import os
import threading
import time

from connectors.webhook.webhook import start_api_service
from utils.fileWatcher import start_file_watcher


def initialize_watcher():
    config_path = 'config/series.yaml'
    while not os.path.exists(config_path):
        time.sleep(1)
    watcher_thread = threading.Thread(target=start_file_watcher)
    watcher_thread.daemon = True  # Esto asegura que el hilo se cierre cuando el programa principal termine
    watcher_thread.start()


def initialize_api_service():
    config_path = 'config/plundarr.conf'
    while not os.path.exists(config_path):
        time.sleep(1)
    webhook_thread = threading.Thread(target=start_api_service)
    webhook_thread.daemon = True  # Esto asegura que el hilo se cierre cuando el programa principal termine
    webhook_thread.start()
