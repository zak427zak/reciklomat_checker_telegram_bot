import requests


def get_user_help(message):
    url = f"http://reciklomat_api:8000/help"
    headers = {'Content-Type': 'application/json'}
    data = {"userId": message.from_user.id}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
