import json

import requests

data = {
    "login": "BordyugM7",
    "password": "s^P24F_k"
}

print(requests.post("http://127.0.0.1:5000/api/auth", json=data).json())