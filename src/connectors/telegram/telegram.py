import logging

import requests

from managers.saveManager import read_conf

logger = logging.getLogger('TelegramConnector')


class Telegram:
    def __init__(self):
        config_parser = read_conf()
        telegram_config = config_parser['telegram']

        self.bot_token = telegram_config.get("bot_token")
        self.chat_id = telegram_config.get("chat_id")

        if not self.bot_token or not self.chat_id:
            logger.error("Faltan datos de configuración para Telegram en config.yaml")

        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, message):
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al enviar mensaje: {e}")
