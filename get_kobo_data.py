import requests
import json
from time import sleep

def get_kobo_data(tries=0):
    if tries > 1000: return False

    with open('tokens.json') as f:
        data = json.load(f)

    auth_token = data["auth_token"]
    form_uid = data["form_uid"]

    headers = {'Authorization': f'Token {auth_token}', 'Content-Type': 'application/json'}
    try:
        r = requests.get(f'https://kf.kobotoolbox.org/api/v2/assets/{form_uid}/data/?format=json', headers=headers, timeout=10)
        registries = r.json()
    except Exception as e:
        print(e)
        sleep(0.1)
        return get_kobo_data(tries + 1)

    return registries["results"]