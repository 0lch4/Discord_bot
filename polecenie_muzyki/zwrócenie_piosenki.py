import os
import requests
import base64
import json

# wpisz tutaj zmienne srodowiskowe ktore przechowuja id klienta i sekret na api spotify
client_id = os.environ.get('Spotify_client_id')
client_secret = os.environ.get('Spotify_client_secret')

token_url = "https://accounts.spotify.com/api/token"
token_data = {
    "grant_type": "client_credentials"}
token_headers = {
    "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"}

response = requests.post(token_url, data=token_data, headers=token_headers)
print("Oto dostępne gatunki:")
with open('polecenie_muzyki\gatunek.json') as f:
    genre = json.load(f)
    
genre = genre.lower()

if response.status_code == 200:
    access_token = response.json()['access_token']
    with open('wynik3.json') as f:
        new_data = json.load(f)
       
    tempo = new_data['tempo']
    loudness = new_data['loudness']
    valence = new_data['valence']
    energy = new_data['energy']
    time_signature = new_data['time_signature']
    mode = new_data['mode']
    key = new_data['key']
    danceability=new_data['danceability']
    speechiness=new_data['speechiness']
    instrumentalness=new_data['instrumentalness']
    popularity=new_data['popularity']

    headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"}

    params = {
        'limit': 3,
        'market': 'PL',
        'q': 'lang:pl',
        'seed_genres': genre,
        'target_tempo': tempo,
        'target_loudness': loudness,
        'target_valence': valence,
        'target_energy': energy,
        'target_time_signature': time_signature,
        'mode': mode,
        'key': key,
        'danceability':danceability,
        'speechiness':speechiness,
        'instrumentalness':instrumentalness,
        'popularity':popularity,
        'type': 'track',
    }
    response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers, params=params, verify=True)
    if response.status_code == 200:
        results = response.json()["tracks"]
        wyniki = response.json()["tracks"]
        if len(results) == 0:
            print("Nie znaleziono utworów dla podanych parametrów wyszukiwania.")
            quit()
        else:
            i=1
            for track in results:
                print(f"\nMiejsce {i}")
                print(f"Utwór: {track['name']}")
                print(f"Wykonawca: {track['artists'][0]['name']}")
                print(f"Link do utworu: {track['external_urls']['spotify']}")
                i+=1
            tracks_info=[]
            for track in wyniki: 
                track_info = {
                "miejsce": i,
                "utwór": track['name'],
                "wykonawca": track['artists'][0]['name'],
                "link": track['external_urls']['spotify']}
                tracks_info.append(track_info)
                with open('wynik4.json','w', encoding='utf-8') as f:
                    json.dump(tracks_info, f, indent=4)
                    
    else:
        print(f"Nie udało się uzyskać wyników wyszukiwania. Kod statusu: {response.status_code}")
        
