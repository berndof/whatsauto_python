import requests
import json

url = 'http://localhost:21465/api/test_session/send-message'

headers = {
    'accept': '*/*',
    'Authorization': 'Bearer $2b$10$wuy4_YHe38Wi9Y6H8BNtLOXt6Fj29QOrg_PtkV6L3rVUwr2ohADly',
    'Content-Type': 'application/json'
}

payload = {
    "phone": "554999255718",
    "isGroup": False,
    "isNewsletter": False,
    "message": "Hi from WPPConnect"
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print('Request successful!')
    print(response.json())
else:
    print(response.status_code)