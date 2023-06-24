# Discord bot ![GitHub forks](https://img.shields.io/badge/Version-1.2.0-red)

Interface in Polish lang

# Opis

Bot na Discorda, posiada on:

-pare wbudowanych komend tekstowych

-możliwość uruchomienia piosenki na Spotify

-możliwość polecenia piosenki na Spotify

-możliwość zarządzania użytkownikami na serwerze

-prosty model nauki, można go nauczyć jak ma odpowiadać na dane kwestie

-możliwość oduczenia go nauczonej rzeczy

-możliwość podania aktualnej pogody w podanym mieście

-możliwość opowiedzenia ciekawostki

## Komendy można zobaczyć wpisując !pomocy

## Licencja

Aplikacja działa na licencji MIT

# Instalacja


## Kopiowanie repozytorium:

```
git clone https://github.com/0lch4/Discord_bot.git
```

## Instalacja bibliotek:

Wymagane jest narzędzie `poetry`:

```
pip install poetry
```

Następnie w głównej lokalizacji wpisujemy

```
poetry install
```

Gdy zależności są zainstalowane należy uruchomić wirtualne środowisko

```
poetry shell
```

## Plik .env:

Należy stworzyć plik `.env` na podstawie `.env.example`

`SPOTIFY_ID` i `SPOTIFY_SECRET` można pozyskać [tutaj](https://developer.spotify.com/)

`BOT_TOKEN` można pozyskać [tutaj](https://discord.com/developers/applications), po uzyskaniu tokenu, należy ustawić botu uprawnienia administratora oraz dodać go do serwera. Wszystko jest dostępne z tego linku.

`BOT_NAMES` to imiona bota na które będzie reagował

`GIRLFRIEND_NAME` to imie dziewczyny, której będzie prawił komplementy

# Uruchamianie

Gdy wszystkie zależności zostały spełnione wpisujemy w głównej lokalizacji:

```
python -m bot.bot
```

## Uruchamianie w kontenerze

Aby zbudować kontener należy wpisać w głównej lokalizacji:

```
docker build -t bot .
```

Następnie aby uruchomić kontener:

```
docker run --env-file .env -d bot
```
