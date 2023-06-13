from dotenv import load_dotenv
import requests
import os
import base64
from requests.models import Response


def conn() -> Response:
    load_dotenv()
    client_id = os.getenv("SPOTIFY_ID")
    client_secret = os.getenv("SPOTIFY_SECRET")

    # polaczenie ze spotify
    token_url = "https://accounts.spotify.com/api/token"  # noqa: S105
    token_data = {"grant_type": "client_credentials"}
    token_headers = {
        "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"  # type: ignore  # noqa: E501
    }
    return requests.post(  # noqa: S113
        token_url, data=token_data, headers=token_headers
    )
