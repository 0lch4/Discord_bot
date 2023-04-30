import os
import requests
import base64
import pytest

# wpisz tutaj zmienne srodowiskowe ktore przechowuja id klienta i sekret na api spotify
client_id = os.environ.get('Spotify_client_id')
client_secret = os.environ.get('Spotify_client_secret')

token_url = "https://accounts.spotify.com/api/token"
token_data = {
    "grant_type": "client_credentials"}
token_headers = {
    "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"}

response = requests.post(token_url, data=token_data, headers=token_headers)
headers = {
    "Authorization": f"Bearer {response.json()['access_token']}",
    "Content-Type": "application/json"}

with open('gatunki.txt') as f:
    genres = [genre.strip().lower() for genre in f]

@pytest.mark.parametrize("genre", genres)
def test_recommendations(genre):
    params = {
        'limit': 1,
        'market': 'PL',
        'seed_genres': genre,
        'target_tempo': 120,
        'target_loudness': -5,
        'target_valence': 0.5,
        'target_energy': 0.5,
        'target_time_signature': 4,
        'mode': 'minor',
        'type': 'track'
    }
    
    response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers, params=params, verify=True)
    assert response.status_code == 200, f"Nie udało się uzyskać wyników wyszukiwania dla gatunku {genre}. Kod statusu: {response.status_code}"
    results = response.json()["tracks"]
    assert len(results) > 0, f" {genre} nie jest gatunkiem obsługiwanym na spotify"
    