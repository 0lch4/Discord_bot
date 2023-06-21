import requests
import json
from pathlib import Path
import sys
from music_recomendation.connection.connection import conn


def get_song() -> None | str:
    title = sys.argv[1]
    artist = sys.argv[2]
    response = conn()
    if response.status_code != 200:
        return f"Błąd {response.status_code}: {response.reason}"
    access_token = response.json()["access_token"]
    while True:
        # wczytywana jest nazwa utworu zapisana w pliku i wysylana w żądaniu
        query = f"track:{title} artist:{artist}"
        search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(search_url, headers=headers)  # noqa: S113
        # sprawdza czy taka piosenka istnieje na spotify
        if response.status_code != 200:
            return f"Błąd {response.status_code}: {response.reason}"

        data = response.json()
        if not data["tracks"]["items"]:
            return "No matching results"
            # wysyla żądanie o dane utworu
        track_id = data["tracks"]["items"][0]["id"]
        features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        popularity_url = f"https://api.spotify.com/v1/tracks/{track_id}"
        response = requests.get(features_url, headers=headers)  # noqa: S113
        popularity_response = requests.get(  # noqa: S113
            popularity_url, headers=headers
        )
        # pobiera właściwości piosenki i zapisuje do pliku wynik2.json
        if response.status_code != 200 or popularity_response.status_code != 200:
            return f"Błąd features{response.status_code} lub popularity{popularity_response.status_code}"  # noqa: E501
        data = response.json()
        popularity_data = popularity_response.json()
        file_path = Path("music_recomendation/datas/results/result2.json")
        with file_path.open(mode="w", encoding="utf-8") as f:
            json.dump(
                {
                    "tempo": data["tempo"],
                    "valence": data["valence"],
                    "loudness": data["loudness"],
                    "energy": data["energy"],
                    "danceability": data["danceability"],
                    "speechiness": data["speechiness"],
                    "time_signature": data["time_signature"],
                    "mode": data["mode"],
                    "key": data["key"],
                    "instrumentalness": data["instrumentalness"],
                    "popularity": popularity_data["popularity"],
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
            break


if __name__ == "__main__":
    get_song()
