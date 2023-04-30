import os
import requests
import base64
import json
import subprocess

# wpisz tutaj zmienne srodowiskowe ktore przechowuja id klienta i sekret na api spotify
client_id = os.environ.get('Spotify_client_id')
client_secret = os.environ.get('Spotify_client_secret')


token_url = "https://accounts.spotify.com/api/token"
token_data = {
    "grant_type": "client_credentials"}
token_headers = {
    "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"}
response = requests.post(token_url, data=token_data, headers=token_headers)

if response.status_code == 200:
    access_token = response.json()['access_token']
    while True:
        with open('wynik.json') as f:
            tytul = json.load(f)
        query = f"track:{tytul}"
        search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"}
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if len(data['tracks']['items']) == 0:
                break
            else:
                track_id = data['tracks']['items'][0]['id']
                features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
                popularity_url = f"https://api.spotify.com/v1/tracks/{track_id}"
                response = requests.get(features_url, headers=headers)
                popularity_response = requests.get(popularity_url, headers=headers)

                if response.status_code == 200 and popularity_response.status_code == 200:
                    data = response.json()
                    popularity_data = popularity_response.json()
                    with open('wynik2.json', 'w', encoding='utf-8') as f:
                        json.dump({'tempo': data['tempo'], 'valence': data['valence'], 'loudness': data['loudness'], 'energy': data['energy'],
                                'time_signature': data['time_signature'], 'mode': data['mode'], 'key': data['key'], 'danceability': data['danceability'],
                                'speechiness': data['speechiness'], 'instrumentalness': data['instrumentalness'], 'popularity': popularity_data['popularity']}, f, indent=2, ensure_ascii=False)
                    break
                else:
                    print(f"Błąd {response.status_code}: {response.reason}")
                    break
        else:
            print(f"Błąd {response.status_code}: {response.reason}")
            break
else:
    print(f"Błąd {response.status_code}: {response.reason}")
    