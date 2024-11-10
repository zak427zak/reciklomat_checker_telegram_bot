import requests


def add_or_remove_item_service(user_id, address):
    url = f"http://reciklomat_api:8000/user/subscribe"
    headers = {'Content-Type': 'application/json'}
    data = {"telegram_id": user_id, "address": address}
    requests.post(url, headers=headers, json=data)
