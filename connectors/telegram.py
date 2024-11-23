import requests
import yaml


class Telegram:
    def __init__(self, config_path="config/config.yaml"):
        """
        Inicializa el bot de Telegram leyendo los datos del archivo de configuración.

        :param config_path: Ruta al archivo config.yaml.
        """
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
            telegram_config = config.get("telegram", {})
            self.bot_token = telegram_config.get("bot_token")
            self.chat_id = telegram_config.get("chat_id")

        if not self.bot_token or not self.chat_id:
            raise ValueError("Faltan datos de configuración para Telegram en config.yaml")

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
            print(f"Error al enviar mensaje: {e}")


def activate_telegram(telegram_information):
    if telegram_information['bot_token'] and telegram_information['bot_token'] != "YOUR_BOT_TOKEN_FROM_TELEGRAM":
        if telegram_information['chat_id'] and telegram_information['chat_id'] != "YOUR_TELEGRAM_CHAT_ID":
            print("telegram se activa")
            return True
        else:
            print("telegram no se activa")
            return False
    else:
        print("telegram no se activa")
        return False
