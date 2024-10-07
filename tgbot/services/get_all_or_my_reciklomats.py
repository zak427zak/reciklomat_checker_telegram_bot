import requests


def get_all_or_my_reciklomats_service(user_id, how_many):
    url = "http://reciklomat_api:8000/check"
    headers = {'Content-Type': 'application/json'}
    data = {"userId": user_id, "howMany": how_many}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result'], r.status_code
    else:
        return r.json()['errorMessage'], r.status_code
