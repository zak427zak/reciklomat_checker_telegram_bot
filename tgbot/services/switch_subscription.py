import requests


def switch_subscription_service(user_id, switch_type):
    url = f"http://reciklomat_api:8000/user/switch/{switch_type}"
    headers = {'Content-Type': 'application/json'}
    data = {"userId": user_id}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
