import logging
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from managers.saveManager import load_series_list
from managers.seriesManager import download_series
from utils.configuration.validateConfig import validate_series_yaml

logger = logging.getLogger('fileWatcher')


class WatcherHandler(FileSystemEventHandler):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def on_modified(self, event):
        monitored_path = os.path.normpath(self.filepath)
        event_path = os.path.normpath(event.src_path)
        if event.src_path == monitored_path:
            logger.info(f"Archivo modificado: {monitored_path}")
            process_wished_series()


def start_file_watcher(config_file="config/series.yaml"):
    event_handler = WatcherHandler(config_file)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(config_file), recursive=False)
    observer.start()
    logger.info(f"Monitoreando cambios en: {config_file}")
    try:
        while True:
            time.sleep(1)  # Mantener el hilo activo
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def process_wished_series():
    print('ejecutamos comando')
    wished_series_list = load_series_list()
    for wished_series in wished_series_list:
        if validate_series_yaml(wished_series):
            download_series(wished_series)
