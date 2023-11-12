# python workflow on requesting token and api data
# author: Carl von Holly
import requests

url = "https://accounts.spotify.com/api/token"
client_id = '54cfccda4e9943e5a50fcbe7fe29b695'
client_secret = '8742fe77513d42809fe3b6cb1acaa30a'

payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(url, data=payload, headers=headers)

# Process the response as needed
print(response.status_code)
print(response.json())

token = response.json()['access_token']

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',  # Adjust the content type as needed
}

r = requests.get('https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb', headers=headers)

print('Artist request response:')
print(r.json())