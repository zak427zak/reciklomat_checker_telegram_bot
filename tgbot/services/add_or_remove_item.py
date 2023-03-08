import requests

from tgbot.config import load_config


def add_or_remove_item_service(user_id, address):
    config = load_config(".env")
    url = f"https://services.llqq.ru/reciklomat/user/subscribe"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}'}
    data = {"userId": user_id, "address": address}
    requests.post(url, headers=headers, data=data)
