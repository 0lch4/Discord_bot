import requests
import json
import html
import os

# podaj tutaj swoja zmienna srodowiskowa ktora przechowuje api yt
api_key = os.environ.get('YouTube_api_key')

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio'}

url = 'https://www.googleapis.com/youtube/v3/search'

with open('nutkaDC.json','r') as f: 
    tytul = f.read()

params = {
    'q': tytul,
    'key': api_key,
    'type': 'music',
    'part': 'id,snippet'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for item in data['items']:
        video_id = item['id']['videoId']
        title = html.unescape(item['snippet']['title'])
        link = f'https://www.youtube.com/watch?v={video_id}'
        with open('nutkaYT.json', 'w', encoding='utf-8') as f:
            json.dump(link, f, indent=2, ensure_ascii=False)
            break
    with open('wynik.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open('wynik.json', 'r', encoding='utf-8') as f:
        plik = f.read()
        for line in plik.splitlines():
            if line.strip().startswith('"title":'):
                line = line.strip()[9:]
                line = line.strip()[1:-2]
                line = html.unescape(line)
                print(line)

else:
    print(f'Błąd {response.status_code}: {response.reason}')
