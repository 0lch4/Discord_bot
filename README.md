# Discord-bot

![GitHub forks](https://img.shields.io/badge/Version-1.1-red)

Interface in Polish lang

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


Aby zbudować obraz Docker zakładając, że Dockerfile znajduje się z resztą plików jak w repozytorium należy wpisać:

docker build -t bot .

Następnie aby uruchomić kontener:

docker run --env-file .env -d bot

Zakładając, że w pliku .env są prawidłowe wartości i znajduje się z resztą plików jak w repozytorium plik .env.example
