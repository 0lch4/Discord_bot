import discord
from discord.ext import commands
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord import FFmpegPCMAudio
import subprocess
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import Any

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

bot_token = os.getenv("BOT_TOKEN")
client_id = os.getenv("SPOTIFY_ID")
client_secret = os.getenv("SPOTIFY_SECRET")
bot_names = os.getenv("BOT_NAMES")
girlfriend_name = os.getenv("GIRLFRIEND_NAME")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
)
"""
listy z zawartoscia
zmienna girlfriend_name przechowuje imie naszej dziewczyny
1 uwzgledniajaca literowki zdania kto jest najpiekniejszy na swiecie, zrobilem aby mojej
dziewczynie bylo milo mozna zedytowac pod swoją
2 zawiera slowa ktore bot napisze po napisaniu olchus i jednego slowa z listy hello_list
3 uwzglednia na co bot ma reagowac, w moim przypadku reaguje na swoją nazwe(nazwalem go olchus)
4 zawiera liste piw, gdy spytasz sie bota jakie dzis wypic poda jedno z tych
mozna tu tworzyc wlasne listy
"""  # noqa: E501

beautiful_list = [
    "kto jest najpiekniejszy na swiecie?",
    "kto jest najpiekniejszy na swiecie",
    "kto jest najpiękniejszy na świecie?",
    "kto jest najpiękniejszy na świecie",
    "kto jest najpiekniejszy na świecie?",
    "kto jest najpiekniejszy na świecie",
    "kto jest najpiękniejszy na swiecie?",
    "kto jest najpiękniejszy na swiecie",
]
hello_list = ["hej", "czesc", "siema", "witaj", "cześć", "elo", "hejka", "hello"]

# w przypadku innej nazwy bota wystarczy zmodyfikowac ta liste
if bot_names:
    bot_names_list = bot_names.split(",")

beer_list = [
    "Żywiec",
    "Tyskie",
    "Lech",
    "Okocim",
    "Warka",
    "Perła",
    "Łomża",
    "Książęce",
    "Harnaś",
    "Pilsner Urquell",
    "Mocne Full",
    "Wojak",
    "Carlsberg",
    "Kasztelan",
    "Radler",
    "Książęce",
    "Redds",
    "Zubr",
    "Desperados",
    "Corona",
    "Piast",
]


# napis pojawiajacy sie w konsoli, ma za zadanie poinformowac ze bot prawidlowo sie uruchomil  # noqa: E501
@bot.event
async def on_ready() -> Any:
    print(f"{bot.user} jestem gotów by ci służyć")


# komenda testowa aby pokazac dostepne opcje
@bot.command(name="pomocy")
async def pomocy(ctx: Any) -> Any:
    await ctx.send(
        """
powitanie: slowo powitalne, nazwa bota
komplement: nazwa bota, 'kto jest najpiekniejszy na swiecie'
polecenie piwa: nazwa bota, 'jakiego browara dzis wypic '
pogoda: nazwa bota, 'ile dzisiaj stopni w ', nazwa miejscowosci
ciekawostka: nazwa bota 'powiedz jakas ciekawostke'
nauka: nazwa bota, ' czas na nauke'
rozmowa z botem na podstawie wyuczoncych rzeczy: 'ej ', nazwa bota, polecenie
oduczenie nauczonej rzeczy: nazwa bota, 'zapomnij o ' nazwa rzeczy na ktora reaguje
wlaczenie muzyki ze spotify: nazwa bota, 'wlacz ',nazwa piosenki
polecenie muzyki ze spotify: nazwa bota, 'polec cos podobnego do ', tytul piosenki, czekanie na odpowiedz bota, wykonawca
wyrzucenie z serwera: nazwa bota, 'wyrzuc z serwera ', nazwa uzytkownika
wyrzucenie z kanalu: nazwa bota, 'wyrzuc z kanalu ', nazwa uzytkownika
wycieszenie: nazwa bota, 'wycisz ', nazwa uzytkownika
wylaczenie dzwieku: nazwa bota, 'wylacz dzwiek ', nazwa uzytkownika
zmiana nazwy uzytkownika: nazwa bota, 'zmien nazwe ', nazwa uzytkownika, nowa nazwa uzytkownika
przeniesienie na inny kanal: nazwa bota, 'przenies ', nazwa uzytkownika, kanal docelowy
"""  # noqa: E501
    )


# obsluga polecen, mozna dodawac tutaj swoje
@bot.event
async def on_message(message: Any) -> Any:  # noqa: C901, PLR0912, PLR0915
    if message.author == bot.user:
        return

    # wbudowana obsluga tekstowa

    """fragment odpowiedzialny za powitanie po napisaniu slowa z listy powitanie
    oraz slowa z listy bot_names_list np hej olchus bot przywita sie z nami
    """
    if any(message.content.lower().startswith(p) for p in hello_list) and any(
        i in message.content.lower() for i in bot_names_list
    ):
        await message.channel.send(random.choice(hello_list))  # noqa: S311

    """fragment odpowiedzialny za prawienie komplementow naszej dziewczynie
    po napisaniu slowa z listy beautiful_list bot zwroci wiadomosc ze jest
    ona najpiekniejsza
    """
    if any(message.content.lower().startswith(i) for i in bot_names_list) and any(
        p in message.content.lower() for p in beautiful_list
    ):
        await message.channel.send(f"Proste, że {girlfriend_name} <3")

    """fragment odpowiedzialny za losowanie piwa, po napisaniu slowa z listy
    bot_names_list oraz jakiego browara dzis wypic losuje piwo z listy beer_list
    """
    if any(
        message.content.lower().startswith(f"{i} jakiego browara dzis wypic")
        for i in bot_names_list
    ):
        await message.channel.send(
            f"dawaj wypij {random.choice(beer_list)}"  # noqa:S311
        )

    """fragment kodu odpowiedzialny za chwalenie tworcy,
       gdy ktos pochwali bota bot chwali autora za pomysl i sporo poswieconego czasu"""
    if any(
        message.content.lower().startswith(f"{i} super jestes") for i in bot_names_list
    ):
        await message.channel.send("jak moj tworca")

    """fragment kodu odpowiedzialny za wyswietlanie aktualenj temperatury,
    wyswietla temperature w twoim miescie, w moim przypadku jest ustawione na Milicz
    pobieranie temperatury nastepuje ze strony https://dobrapogoda24.pl/
    """
    if any(
        message.content.lower().startswith(f"{i} ile dzisiaj stopni w ")
        for i in bot_names_list
    ):
        city = message.content.lower().split("ile dzisiaj stopni w ")[1]
        weather = requests.get(f"https://dobrapogoda24.pl/pogoda/{city}")  # noqa: S113
        soup = BeautifulSoup(weather.text, "lxml")
        try:
            temperature = soup.select(".tab_temp_max")[0]
            await message.channel.send(f"w {city} jest dzis {temperature.text}")
        except IndexError:
            await message.channel.send("nie widze takiej miejscowosci")

    """fragment kodu odpowiedzialny za opowiedzenie ciekawostki,
    losuje ciekawostke ze strony https://fajnepodroze.pl/glupie-ciekawostki/
    """
    if any(
        message.content.lower().startswith(f"{i} powiedz jakas ciekawostke")
        for i in bot_names_list
    ):
        fun_fact = requests.get("https://fajnepodroze.pl/glupie-ciekawostki/")  # noqa: S113, E501
        soup = BeautifulSoup(fun_fact.text, "lxml")
        lanes = soup.find_all("p")
        facts = []
        for fact in lanes:
            facts.append(fact.text)
        while True:
            result = random.choice(facts)  # noqa: S311
            if not result[0]:
                continue
            if result[0].isdigit():
                await message.channel.send(result[3:])
                break

    # nauka

    """fragment kodu ktory umozliwia uczenia bota nowych fraz
    gdy podamy slowo z listy bot_names_list i napiszemy czas na nauke
    bot spyta sie na co ma reagowac i nastepna wiadomosc ktora napiszemy
    zostanie zapisana do zmiennej reaction nastepnie bot sie spyta jak ma odpowiadac
    i nastepna wiadomosc ktora napiszemy zostanie zapisana do zmiennej odpowiedz
    """
    if any(
        message.content.lower().startswith(f"{i} czas na nauke") for i in bot_names_list
    ):
        await message.channel.send("na co mam reagować?")
        reaction = await bot.wait_for(
            "message", check=lambda m: m.author == message.author
        )
        await message.channel.send("jak mam odpowiadać?")
        answer = await bot.wait_for(
            "message", check=lambda m: m.author == message.author
        )

        # bot otwiera swoj zbior danych
        file_path = Path("bot/bot_datas/data.json")
        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)

        # utworzenie slownika gdzie do slow na ktore ma reagowac jest przypisana odpowiedz  # noqa: E501
        interaction = {reaction.content: answer.content}

        """bot sprawdza czy klucz na ktory ma reagowac jest w jego zbiorze danych jesli
        jest odpowiada nam ze wie co ma mowic jesli nie ma zapisuje nam slowa na ktore
        ma reagowac i odpowiedz na nia do pliku data
        """
        if not any(inter == interaction for inter in data):
            data.append(interaction)
            file_path = Path("bot/bot_datas/data.json")
            with file_path.open(mode="w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            await message.channel.send("dobra zapamiętałem")
        else:
            await message.channel.send("juz wiem co mam na to odpowiedziec")

    """po napisaniu ej i slowa z listy bot_names_list a nastepnie dowolnych slow bot
    sprawdzi czy umie na nie odpowiedziec jesli nie to poinformuje nas o tym jesli
    tak to odpowie namflaga czy_jest sprawdza czy takie slowo jest w bazie
    """
    is_it = False
    if any(message.content.lower().startswith(f"ej {i}") for i in bot_names_list):
        instruction = message.content[10:]
        file_path = Path("bot/bot_datas/data.json")
        with file_path.open(mode="r", encoding="utf-8") as f:
            learn = json.load(f)
        for lrn in learn:
            if instruction in lrn:
                is_it = True
                await message.channel.send(lrn[instruction])

        if is_it is False:
            await message.channel.send("nie umiem nic takiego ale mozesz mnie nauczyc")

    """fragment ktory umozliwa oduczcenia czegos bota
    po napisaniu slowa z bot_names_list i napisaniu zapomnij o usuwa klucz ze swojej bazy
    i informuje nas ze o tym zapomina
    jesli nie ma takiego klucza poinformuje nas o tym
    gdy kazemu mu zapomniec o jakims slowie nie bedzie juz na nie reagowal
    flaga bylo sprawdza czy takie slowo bylo w bazie"""
    was = False
    if message.content.lower().startswith(
        tuple(f"{i} zapomnij o " for i in bot_names_list)
    ):
        forget = message.content.lower().split("zapomnij o ")[1]
        file_path = Path("bot/bot_datas/data.json")
        with file_path.open(encoding="utf-8") as f:
            forgot = json.load(f)
        for frg in forgot:
            if forget in frg:
                was = True
                frg.pop(forget)
                await message.channel.send("no to zapominam")
        if was is False:
            await message.channel.send("ja nawet nic takiego nie umiem xD")
        # zapisuje zmienione dane lub pozostawia stare dane jesli nie mial takiego klucza  # noqa: E501
        file_path = Path("bot/bot_datas/data.json")
        with file_path.open(mode="w", encoding="utf-8") as f:
            json.dump(forgot, f, ensure_ascii=False, indent=4)

    # obsluga muzyczna

    """fragment odpowiedzialny za wyszukiwanie piosenek na spotify
       po podaniu tytulu i wykonawcy lub tytulu wyszuka i odtworzy piosenke
       niestety aktualnie sa to tylko wersje probkowe piosenek i jest problem z
       uruchomieniem calych piosenek gdy chcialem uruchomic cala pokazuje ze bot gra na
       kanale jedak nic nie slychac a w konsoli pojawia sie
       discord.player ffmpeg process 9072 successfully terminated with return code of 1.
       9072 nie jest stałą, te liczby sie zmieniaja
       jak tylko znajde rozwiazanie problemu to je udostepnie"""

    # fragment ktory wylapuje wiadomosc na czacie ktora sie zaczyna od slowa z bot_name_
    # list i slowa wlacz
    if message.content.lower().startswith(tuple(f"{i} wlacz " for i in bot_names_list)):
        # rozdzielenie powyzszej czesci i slow ktore zostaly wprowadzone
        song = message.content.lower().split("wlacz ")[1]

        # wyszukuje piosenke o podanym tytule i pobiera pierwsza
        results = sp.search(q=song, limit=1, type="track")

        # sprawdza czy szukany rezultat istnieje
        if results["tracks"]["items"]:  # type:ignore
            # pobiera utwor i pobiera jego identyfikator
            track_uri = results["tracks"]["items"][0]["uri"]  # type:ignore
            audio_url = sp.track(track_uri)["preview_url"]  # type:ignore

            # informuje uzytkownika ze znalazlo piosenke
            if audio_url is not None:
                await message.channel.send("no pewnie")

                """sprawdza czy uzytkownik jest na kanale muzyka moze byc puszczona
                tylko na kanale gdzie on sie znajduje jesli bota nie ma na kanale to go
                dodaje i odtwarza on piosenke jesli bot jest juz na kanale to go
                rozlacza i odrazu dodaje i odtwarza on piosenke
                """
                if not message.author.voice:
                    await message.channel.send("ale na kanal pierw wejdz")
                    return
                channel = message.author.voice.channel
                if message.guild.voice_client:
                    await message.guild.voice_client.disconnect()
                vc = await channel.connect(reconnect=True, timeout=10.0)
                vc.play(FFmpegPCMAudio(audio_url + "&play=true", options="-vn"))
            else:
                # jesli szukany rezultat nie istnieje informuje o tym
                await message.channel.send("nie widze takiej")
        else:
            # jesli szukany rezultat nie istnieje informuje o tym
            await message.channel.send("nie widze takiej")

    """fragment odpowiedzialny za polecanie piosenki na podstawie jednej podanej
    ta funkcja korzysta z innej aplikacji do polecania muzyki ktora dostosowalem
    do potrzeb bota
       """

    # po napisaniu slowa z listy bot_names_list i slow polec cos podobnego rozdziela
    # tekst aby jego druga czesc zawierala tytul
    if message.content.lower().startswith(
        tuple(f"{i} polec cos podobnego do " for i in bot_names_list)
    ):
        title = message.content.lower().split("polec cos podobnego do ")[1]

        # nastepnie pyta o wykonawce
        await message.channel.send("pewnie podaj mi jeszcze wykonawce")

        artist = await bot.wait_for(
            "message", check=lambda m: m.author == message.author
        )

        # uruchamia aplikacje do pozyskania linku i parametrow utworu,
        # przekazuje jako argument wykonawce i tytul
        subprocess.run(
            [  # noqa: S603, S607
                "python",
                "-m",
                "music_recomendation.music_app.song_analize",
                title,
                artist.content,
            ]
        )

        # jesli sie to powiedzie bot informuje na czacie ze mysli
        await message.channel.send("dobra mysle czaj")

        # uruchamia aplikacje z siecia neuronowa ktora przetwarza dane o utworze i
        # dobiera parametry aby dac podobny
        subprocess.run(
            [  # noqa: S603, S607
                "python",
                "-m",
                "music_recomendation.music_app.neural",
            ]
        )

        # pyta uzytkownika o wybranie gatunku muzycznego,
        # ktory chce otrzymac i wypisuje dostepne
        await message.channel.send("dobra a gatunek jaki chcesz miec? masz do wyboru:")
        file_path = Path("music_recomendation/datas/genres.txt")
        with file_path.open(mode="r") as f:
            for genre in f:
                await message.channel.send(genre)

        # informuje ze w przypadku blednych danych da ostatnie wyniki
        await message.channel.send(
            """jak jakis smieszek da inny niz z listy albo nieistniejaca piosenke dam jakies stare i tyle xD"""  # noqa: E501
        )

        # zapisuje ostatnia wiadomosc uzytkownika do zmiennej i nastepnie
        # zapisuje ja do pliku gatunek.json
        genre = await bot.wait_for(
            "message", check=lambda m: m.author == message.author
        )

        # uruchamia aplikacje ktora wysyla nowe dane do spotify i pobiera odpowiednie
        # piosenki, przekazuje jako argument nazwe gatunku
        subprocess.run(
            [  # noqa: S607, S603
                "python",
                "-m",
                "music_recomendation.music_app.new_parameters",
                genre.content,
            ]
        )

        # odczytuje 3 najbardzije pasujace piosenki z wynik4.json i wyswietla na kanale
        file_path = Path("music_recomendation/datas/results/result4.json")
        with file_path.open(encoding="utf-8") as f:
            recomendation = json.load(f)
            place = 1
        for recomend in recomendation:
            title = recomend["utwór"]
            author = recomend["wykonawca"]
            link = recomend["link"]
            await message.channel.send(f"Miejsce: {place}\n{title} - {author}\n{link}")
            place += 1

    # obsluga uzytkownikow

    """po napisaniu wyrzuc z serwera oraz nazwy uzytkownika  uzytkownik jest usuwany
    z serwera gdy nie ma takiego uzytkownika lub nazwa jest blednie wpisana pojawia sie
    wiadomosc ze bot go nie widzi
    """
    if any(
        message.content.lower().startswith(f"{i} wyrzuc z serwera")
        for i in bot_names_list
    ):
        kick = message.content.split()[4]
        member = message.guild.get_member_named(kick)
        if member:
            await member.kick(reason="naura")
            await message.channel.send(f"{kick} juz nie bedzie sprawial problemow")
        else:
            await message.channel.send(f"Nie widze {kick}")

    """po napisaniu wyrzuc z kanalu oraz nazwy uzytkownika  uzytkownik jest usuwany
    z kanalu gdy nie ma takiego uzytkownika lub nazwa jest blednie wpisana pojawia
    sie wiadomosc ze bot go nie widzi
    """
    if any(
        message.content.lower().startswith(f"{i} wyrzuc z kanalu")
        for i in bot_names_list
    ):
        kick = message.content.split()[4]
        member = message.guild.get_member_named(kick)
        if member:
            await member.move_to(None)
            await message.channel.send(f"{kick} juz nie bedzie przeszakadzac")
        else:
            await message.channel.send(f"Nie widze {kick}")

    """po napisaniu wycisz oraz nazwy uzytkownika uzytkownik jest wyciszany
    gdy nie ma takiego uzytkownika lub nazwa jest blednie wpisana pojawia
    sie wiadomosc ze bot go nie widzi"""
    if any(message.content.lower().startswith(f"{i} wycisz") for i in bot_names_list):
        mute = message.content.split()[2]
        member = message.guild.get_member_named(mute)
        if member:
            await member.edit(mute=True)
            await message.channel.send(f"{mute} juz nie bedzie gderal")
        else:
            await message.channel.send(f"Nie widze {mute}")

    """po napisaniu wylacz dzwiek oraz nazwy uzytkownika uzytkownik jest ma wylaczony
    dzwiek gdy nie ma takiego uzytkownika lub nazwa jest blednie wpisana pojawia sie
    wiadomosc ze bot go nie widzi
    """
    if any(
        message.content.lower().startswith(f"{i} wylacz dzwiek") for i in bot_names_list
    ):
        mute = message.content.split()[3]
        member = message.guild.get_member_named(mute)
        if member:
            await member.edit(deafen=True)
            await message.channel.send(f"{mute} teraz juz cie nie uslyszy")
        else:
            await message.channel.send(f"Nie widze {mute}")

    """po napisaniu zmien nazwe oraz nazwy uzytkownika bot pyta na co ma zmienic nazwe
    podanego uzytkownika i wykonuje polecenie gdy nie ma takiego uzytkownika lub nazwa
    jest blednie wpisana pojawia sie wiadomosc ze bot go nie widzi
    """
    if any(
        message.content.lower().startswith(f"{i} zmien nazwe") for i in bot_names_list
    ):
        name = message.content.split()[3]
        member = message.guild.get_member_named(name)
        if member:
            await message.channel.send("a jak go nazwac?")
            new_name = await bot.wait_for(
                "message", check=lambda m: m.author == message.author
            )
            await member.edit(nick=new_name.content)
            await message.channel.send(f"{name} to od teraz teraz {new_name.content}")
        else:
            await message.channel.send(f"Nie widze {name}")

    """po napisaniu przenies oraz nazwy uzytkownika bot pyta na jaki kanal go przeniesc
    i wykonuje polecenie gdy nie ma takiego uzytkownika lub nazwa jest blednie wpisana
    pojawia sie wiadomosc ze bot go nie widzi
    """
    if any(message.content.lower().startswith(f"{i} przenies") for i in bot_names_list):
        move = message.content.split()[2]
        member = message.guild.get_member_named(move)
        if member:
            await message.channel.send("a gdzie?")
            new_channel = await bot.wait_for(
                "message", check=lambda m: m.author == message.author
            )
            channel = discord.utils.get(
                message.guild.channels, name=new_channel.content
            )
            if channel:
                await member.move_to(channel)
                await message.channel.send(
                    f"{move} został przeniesiony na kanał {channel.name}"
                )
            else:
                await message.channel.send(
                    f"Nie znaleziono kanału o nazwie {new_channel.content}"
                )
        else:
            await message.channel.send(f"Nie widzę {move}")

    # sprawdza czy wiadomosc zawiera komende dla bota
    await bot.process_commands(message)


# token bota, jest wymagany aby bot dzialal

bot.run(bot_token)  # type: ignore
