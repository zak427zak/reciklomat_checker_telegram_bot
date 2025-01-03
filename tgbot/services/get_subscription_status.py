import requests
from aiogram.types import Message


def get_subscription_status(message: Message):
    url = f"http://reciklomat_api:8000/user/status"
    headers = {'Content-Type': 'application/json'}
    data = {"telegram_id": message.from_user.id}
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
