import requests
import json
from pathlib import Path
import sys
from music_recomendation.connection.connection import conn


def new_song() -> None | str:
    genre = sys.argv[1].lower()
    response = conn()
    if response.status_code != 200:
        return f"Błąd {response.status_code}: {response.reason}"
    access_token = response.json()["access_token"]
    # laduje nowe dane utworu
    file_path = Path("music_recomendation/datas/results/result3.json")
    with file_path.open(mode="r") as f:
        new_data = json.load(f)
    # przypisuje wlasciwosci piosenki do zmiennych
    tempo = new_data["tempo"]
    valence = new_data["valence"]
    loudness = new_data["loudness"]
    energy = new_data["energy"]
    danceability = new_data["danceability"]
    speechiness = new_data["speechiness"]
    time_signature = new_data["time_signature"]
    mode = new_data["mode"]
    key = new_data["key"]
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
    if response.status_code != 200:
        return f"Błąd {response.status_code}: {response.reason}"
    wyniki = response.json()["tracks"]
    # sprawdza czy taka piosenka istnieje
    if not wyniki:
        return "No matching results"
    place = 1
    tracks_info = []
    for track in wyniki:
        track_info = {
            "miejsce": place,
            "utwór": track["name"],
            "wykonawca": track["artists"][0]["name"],
            "link": track["external_urls"]["spotify"],
        }
        tracks_info.append(track_info)
        place += 1
        # zapisuje do pliku wynik4.json
    file_path = Path("music_recomendation/datas/results/result4.json")
    with file_path.open(mode="w", encoding="utf-8") as f:
        json.dump(tracks_info, f, indent=4)
        return None


if __name__ == "__main__":
    new_song()
