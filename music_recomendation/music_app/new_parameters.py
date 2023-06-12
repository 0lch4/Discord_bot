import os
import sys
import requests
import base64
import json
from pathlib import Path
from dotenv import load_dotenv
from typing import Any

def new_song() -> Any:
    load_dotenv()
    client_id = os.getenv("SPOTIFY_ID")
    client_secret = os.getenv("SPOTIFY_SECRET")

    # polaczenie ze spotify
    token_url = "https://accounts.spotify.com/api/token"  # noqa: S105
    token_data = {"grant_type": "client_credentials"}
    token_headers = {
        "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"  # type: ignore  # noqa: E501
    }
    response = requests.post(
        token_url, data=token_data, headers=token_headers
    )

    # laduje wybrany gatunek
    file_path = Path("music_recomendation/datas/genre.json")
    with file_path.open(mode="r") as f:
        genre = json.load(f)
    genre = genre.lower()
    # laduje nowe dane utworu
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        file_path = Path("music_recomendation/datas/results/result3.json")
        with file_path.open(mode="r") as f:
            new_data = json.load(f)
        # przypisuje wlasciwosci piosenki do zmiennych
        tempo = new_data["tempo"]
        loudness = new_data["loudness"]
        valence = new_data["valence"]
        energy = new_data["energy"]
        time_signature = new_data["time_signature"]
        mode = new_data["mode"]
        key = new_data["key"]
        danceability = new_data["danceability"]
        speechiness = new_data["speechiness"]
        instrumentalness = new_data["instrumentalness"]
        popularity = new_data["popularity"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        # tworzy parametry ktore sa odczytywane przez strone
        params = {
            "limit": 3,
            "market": "PL",
            "q": "lang:pl",
            "seed_genres": genre,
            "target_tempo": tempo,
            "target_loudness": loudness,
            "target_valence": valence,
            "target_energy": energy,
            "target_time_signature": time_signature,
            "mode": mode,
            "key": key,
            "danceability": danceability,
            "speechiness": speechiness,
            "instrumentalness": instrumentalness,
            "popularity": popularity,
            "type": "track",
        }
        # wysyla zapytanie o piosenke z podanymi parametrami
        response = requests.get(  # noqa: S113
            "https://api.spotify.com/v1/recommendations",
            headers=headers,
            params=params,
            verify=True,
        )
        if response.status_code == 200:
            wyniki = response.json()["tracks"]
            # sprawdza czy taka piosenka istnieje
            if len(wyniki) == 0:
                sys.exit()
            else:
                i = 1
                tracks_info = []
                for track in wyniki:
                    track_info = {
                        "miejsce": i,
                        "utwór": track["name"],
                        "wykonawca": track["artists"][0]["name"],
                        "link": track["external_urls"]["spotify"],
                    }
                    tracks_info.append(track_info)
                    i += 1
                    # zapisuje do pliku wynik4.json
                file_path = Path("music_recomendation/datas/results/result4.json")
                with file_path.open(mode="w", encoding="utf-8") as f:
                    json.dump(tracks_info, f, indent=4)

        else:
            print(
                f"Nie udało się uzyskać wyników wyszukiwania. Kod statusu: {response.status_code}"  # noqa: E501
            )

if __name__ =="__main__":
    new_song()
