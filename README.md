# Discord-bot

![GitHub forks](https://img.shields.io/badge/Version-1.0-red)

Instalacja bibliotek:


pip install -r requirements.txt


Wymagane api keye znajdują się w pliku .env.example
należy utworzyć plik .env i podać tam swoje klucze według wzoru


Bot w moim przypadku reaguje na olchus, bo tak go nazwalem. Aby zmienic slowa na ktore reaguje
należy edytować linie 49 'bot_name_list = ['olchus','olchuś']' i wprowadzic tam swoją nazwe bota


Bot posiada:

pare wbudowanych komend tekstowych

możliwość uruchomienia piosenki na spotify

możliwość polecenia piosenki na spotify

możliwość wyrzucenia użytkownika z serwera

prosty model nauki, gdy powiemy mu co ma pisać na dane słowa będzie to robił

możliwość aby bot zapomniał nauczonych go rzeczy

podaje aktualną pogodę w podanym mieście


komendy można zobaczyć wpisując !pomocy


Aby zbudować obraz docker zakładając, że dockerfile znajduje się z resztą plików jak w repozytorium należy wpisać:

docker build -t discord_bot .

gdzie discord_bot można zmienić według własnych preferencji

Następnie aby uruchomić kontener:

docker run --env-file .env -d discord_bot

Zakładając, że w pliku .env są prawidłowe wartości i znajduje się z resztą plików jak w repozytorium plik .env.example
