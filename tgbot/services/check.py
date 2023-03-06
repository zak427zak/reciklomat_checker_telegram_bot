import requests

from tgbot.config import load_config


def check(user_id, how_many):
    config = load_config(".env")
    url = "https://services.llqq.ru/reciklomat/check"
    headers = {
        'Authorization': f'Bearer {config.tg_bot.server_token}'
    }
    data = {"userId": user_id, "howMany": how_many}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()
    else:
        return r.json()
