import requests

from tgbot.config import load_config


def get_all_or_my_reciklomats_service(user_id, how_many):
    config = load_config(".env")
    url = "https://services.llqq.ru/reciklomat/check"
    headers = {
        'Authorization': f'Bearer {config.tg_bot.server_token}'
    }
    data = {"userId": user_id, "howMany": how_many}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result'], r.status_code
    else:
        return r.json()['errorMessage'], r.status_code
