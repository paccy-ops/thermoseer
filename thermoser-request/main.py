import requests
import json

url = "http://127.0.0.1:8000/api/create"


def post_data(val):
    payload = json.dumps({
        "scanner_id": val[0],
        "temp": val[1]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)
