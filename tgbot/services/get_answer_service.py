import requests

from tgbot.config import load_config


def get_user_help(message):
    config = load_config(".env")
    url = f"https://services.llqq.ru/reciklomat/help"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}'}
    data = {"userId": message.from_user.id}
    r = requests.post(url, headers=headers, data=data)
    return r.json()['errorMessage']
