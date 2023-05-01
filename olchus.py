import discord
from discord.ext import commands
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from discord import FFmpegPCMAudio
import subprocess
import json


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client_id = '7d86accdaa2745c8883da921deac3dde'
client_secret = '06d0ba0d732c4144920b8bb87407e41b'
redirect_uri = "http://localhost:8000"
scope = "user-library-read,user-modify-playback-state,user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

'''
listy z zawartoscia
zmienna imie_dziewczyny przechowuje imie naszej dziewczyny
1 uwzgledniajaca literowki zdania kto jest najpiekniejszy na swiecie, zrobilem aby mojej dziewczynie bylo milo mozna zedytowac pod siebie
2 zawiera slowa ktore bot napisze po napisaniu olchus i jednego slowa z tej listy
3 uwzglednia olchus z polskim znakiem i bez
4 zawiera liste piw, gdy spytasz sie bota jakie dzis wypic poda jedno z tych
mozna tu tworzyc wlasne listy
'''
imie_dziewczyny = 'Olusia'

piekna_list=['kto jest najpiekniejszy na swiecie?',
            'kto jest najpiekniejszy na swiecie',
            'kto jest najpiękniejszy na świecie?',
            'kto jest najpiękniejszy na świecie',
            'kto jest najpiekniejszy na świecie?',
            'kto jest najpiekniejszy na świecie',
            'kto jest najpiękniejszy na swiecie?'
            'kto jest najpiękniejszy na swiecie'
            ]
powitanie_list=['hej','czesc','siema','witaj','cześć','elo','hejka']
olchus_list = ['olchus','olchuś']
browary_list = ['Żywiec', 'Tyskie', 'Lech', 'Okocim', 'Warka', 'Perła', 'Łomża', 'Książęce', 'Harnaś', 'Pilsner Urquell', 'Mocne Full', 'Wojak', 'Carlsberg', 'Kasztelan', 'Radler', 'Książęce','Redds', 'Zubr', 'Desperados','Corona','Piast']

#napis pojawiajacy sie w konsoli, ma za zadanie poinformowac ze bot prawidlowo sie uruchomil
@bot.event
async def on_ready():
    print(f'Witaj mój stwórco to ja {bot.user} jestem gotów by ci służyć')

#komenda testowa aby sprawdzic czy bot dziala, po napisaniu !test powinien wyswietlic test
@bot.command(name='test')
async def test(ctx):
    await ctx.send('test')

#obsluga polecen, mozna dodawac tutaj swoje
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
#wbudowana obsluga tekstowa
    
    '''fragment odpowiedzialny za powitanie
       po napisaniu slowa z listy powitanie oraz slowa z listy olchus_list np hej olchus bot przywita sie z nami'''
    if any(message.content.lower().startswith(p) for p in powitanie_list) and any(o in message.content.lower() for o in olchus_list):
        await message.channel.send(random.choice(powitanie_list))
        
    '''fragment odpowiedzialny za prawienie komplementow naszej dziewczynie
       po napisaniu slowa z listy piekna_ol_list bot zwroci wiadomosc ze jest ona najpiekniejsza'''
    if any(i in message.content.lower() for i in piekna_list):
        await message.channel.send(f'Proste, że {imie_dziewczyny} <3')
        
    '''fragment odpowiedzialny za losowanie piwa, 
       po napisaniu slowa z listy olchus oraz jakiego browara dzis wypic losuje piwo z listy browary_list'''    
    if any(message.content.lower().startswith(f'{i} jakiego browara dzis wypic') for i in olchus_list): 
        await message.channel.send(f'dawaj wypij {random.choice(browary_list)}')  
         
    '''fragment odpowiedzialny za to ze, gdy spytamy bota czy pokaze co potrafi wyswietli napis no jasne
       ma to za zadanie dac wieksze poczucie interaktywnosci'''
    if any(message.content.lower().startswith(f'{i} pokazesz co umiesz?') for i in olchus_list):
        await message.channel.send('no jasne')
        
    '''fragment kodu odpowiedzialny za chwalenie tworcy,
       gdy ktos pochwali bota bot chwali autora za pomysl i sporo poswieconego czasu'''
    if any(message.content.lower().startswith(f'{i} super jestes') for i in olchus_list):
        await message.channel.send('jak moj tworca')
    
#nauka nowych wypowiedzi
    
    '''fragment kodu ktory umozliwia uczenia bota nowych fraz
       gdy podamy slowo z listy olchus_list i napiszemy czas na nauke 
       bot spyta sie na co ma reagowac i nastepna wiadomosc ktora napiszemy zostanie zapisana do zmiennej reakcja
       nastepnie bot sie spyta jak ma odpowiadac i nastepna wiadomosc ktora napiszemy zostanie zapisana do zmiennej odpowiedz
    '''
    if any(message.content.lower().startswith(f'{i} czas na nauke') for i in olchus_list):
        await message.channel.send("na co mam reagować?")
        reakcja = await bot.wait_for('message', check=lambda m: m.author == message.author)
        await message.channel.send("jak mam odpowiadać?")
        odpowiedz = await bot.wait_for('message', check=lambda m: m.author == message.author)

        # bot otwiera swoj zbior danych
        with open('nauka.json', 'r', encoding='utf-8') as f:
            dane = json.load(f)
        
        #utworzenie slownika gdzie do slow na ktore ma reagowac jest przypisana odpowiedz    
        interakcja = {reakcja.content: odpowiedz.content}
            
        '''bot sprawdza czy klucz na ktory ma reagowac jest w jego zbiorze danych
        jesli jest odpowiada nam ze wie co ma mowic
        jesli nie ma zapisuje nam slowa na ktore ma reagowac i odpowiedz na nia do pliku nauka'''
        if not any(i == interakcja for i in dane):
            dane.append(interakcja)
            with open('nauka.json', 'w', encoding='utf-8') as f:
                json.dump(dane, f, ensure_ascii=False, indent=4)
            await message.channel.send("dobra zapamiętałem.")
        else:
            await message.channel.send("juz wiem co mam na to odpowiedziec")
                    
    '''po napisaniu ej i slowa z listy olchus list a nastepnie dowolnych slow bot sprawdzi czy umie na nie odpowiedziec
       jesli nie to nic sie nie dzieje jesli tak to odpowie nam'''        
    if any(message.content.lower().startswith(f'ej {i}') for i in olchus_list):
        polecenie = message.content[10:]
        with open('nauka.json', 'r', encoding='utf-8') as f:
            nauka = json.load(f)
        for i in nauka:
            if polecenie in i:
                 await message.channel.send(i[polecenie])
   
#obsluga muzyczna
    
    '''fragment odpowiedzialny za wyszukiwanie piosenek na spotify
       po podaniu tytulu i wykonawcy lub tytulu wyszuka i odtworzy piosenke
       niestety aktualnie sa to tylko wersje probkowe piosenek i jest problem z uruchomieniem calych piosenek
       gdy chcialem uruchomic cala pokazuje ze bot gra na kanale jedak nic nie slychac a w konsoli pojawia sie
       discord.player ffmpeg process 9072 successfully terminated with return code of 1.
       9072 nie jest stałą, te liczby sie zmieniaja
       jak tylko znajde rozwiazanie problemu to je udostepnie'''
       
    #fragment ktory wylapuje wiadomosc na czacie ktora sie zaczyna od slowa z olchus_list i slowa wlacz   
    if message.content.lower().startswith(tuple(f'{i} wlacz ' for i in olchus_list)):
        
        #rozdzielenie powyzszej czesci i slow ktore zostaly wprowadzone
        nuta = message.content.lower().split('wlacz ')[1]
        
        #wyszukuje piosenke o podanym tytule i pobiera pierwsza
        results = sp.search(q=nuta, limit=1, type='track')
        
        #sprawdza czy szukany rezultat istnieje
        if len(results['tracks']['items']) > 0:
            
            #pobiera utwor i pobiera jego identyfikator 
            track_uri = results['tracks']['items'][0]['uri']
            audio_url = sp.track(track_uri)['preview_url']
            
            #informuje uzytkownika ze znalazlo piosenke
            await message.channel.send('no pewnie')
                        
            '''sprawdza czy uzytkownik jest na kanale
            muzyka moze byc puszczona tylko na kanale gdzie on sie znajduje
            jesli bota nie ma na kanale to go dodaje i odtwarza on piosenke
            jesli bot jest juz na kanale to go rozlaczai odrazu dodaje i odtwarza on piosenke'''
            channel = message.author.voice.channel
            if not message.author.voice:
                await message.channel.send('ale na kanal pierw wejdz')
                return    
            if message.guild.voice_client:
                await message.guild.voice_client.disconnect()
            vc = await channel.connect(reconnect=True, timeout=10.0)
            vc.play(FFmpegPCMAudio(audio_url+"&play=true", executable="ffmpeg.exe", options="-vn"))
        else:
            #jesli szukany rezultat nie istnieje informuje o tym
            await message.channel.send('nie widze takiej')

    '''fragment odpowiedzialny za polecanie piosenki na podstawie jednej podanej
       ta funkcja korzysta z innej aplikacji do polecania muzyki ktora dostosowalem do potrzeb bota'''
       
    # po napisaniu slowa z listy olchus_list i slow polec cos podobnego rozdziela tekst aby jego druga czesc zawierala piosenke
    if message.content.lower().startswith(tuple(f'{i} polec cos podobnego do ' for i in olchus_list)):
        tytul = message.content.lower().split('polec cos podobnego do ')[1]
        
        #zapisuje piosenke  do pliku wynik.json   
        with open('wyniki\wynik.json','w',encoding='utf-8') as f:
            json.dump(tytul,f, indent=2, ensure_ascii=False)    
            
        #uruchamia aplikacje do pozyskania linku i parametrow utworu   
        subprocess.run(["python", "polecenie_muzyki\pobranie_piosenki.py"])
        
        #jesli sie to powiedzie bot informuje na czacie ze mysli    
        await message.channel.send("dobra mysle czaj")
        
        #uruchamia aplikacje z siecia neuronowa ktora przetwarza dane o utworze i dobiera parametry aby dac podobny
        subprocess.run(["python", "polecenie_muzyki\AI.py"])
        
        #pyta uzytkownika o wybranie gatunku muzycznego, ktory chce otrzymac i wypisuje dostepne
        await message.channel.send('dobra a gatunek jaki chcesz miec? masz do wyboru:')
        with open('polecenie_muzyki\gatunki.txt') as f:
                for gatunek in f:
                    await message.channel.send(gatunek)
                    
        #informuje ze w przypadku blednych danych da ostatnie wyniki
        await message.channel.send('jak jakis smieszek da inny niz z listy albo nieistniejaca piosenke dam jakies stare i tyle xD')
        
        #zapisuje ostatnia wiadomosc uzytkownika do zmiennej i nastepnie zapisuje ja do pliku gatunek.json                             
        user_message = await bot.wait_for('message', check=lambda m: m.author == message.author)
        with open('polecenie_muzyki\gatunek.json','w') as f:
                json.dump(user_message.content,f, indent=2, ensure_ascii=False)
                
        #uruchamia aplikacje ktora wysyla nowe dane do spotify i pobiera odpowiednie piosenki       
        subprocess.run(["python", "polecenie_muzyki\zwrócenie_piosenki.py"])
        
        #odczytuje 3 najbardzije pasujace piosenki z wynik4.json i wyswietla na kanale
        with open('wyniki\wynik4.json','r',encoding='utf-8') as f:
                polecane = json.load(f)
                miejsce = 1
        for polecenie in polecane:
                tytul = polecenie['utwór']
                wykonawca = polecenie['wykonawca']
                link = polecenie['link']
                await message.channel.send(f"Miejsce: {miejsce}\n{tytul} - {wykonawca}\n{link}")
                miejsce+=1
                
#obsluga uzytkownikow
    
    '''po napisaniu wyjeb oraz nazwy uzytkownika  uzytkownik jest usuwany z serwera
       gdy nie ma takiego uzytkownika lub nazwa jest blednie wpisana pojawia sie wiadomosc ze bot go nie widzi'''    
    if any(message.content.lower().startswith(f'{i} wyjeb') for i in olchus_list):
        kasacja = message.content.split()[2]  
        member = message.guild.get_member_named(kasacja)
        if member:
            await member.kick(reason='naura')
            await message.channel.send(f'{kasacja} juz nie bedzie sprawial problemow')
        else:
            await message.channel.send(f'Nie widze {kasacja}')

    #sprawdza czy wiadomosc zawiera komende dla bota
    await bot.process_commands(message)
    
#token bota, jest wymagany aby bot dzialal
bot.run('MTEwMTQ3MTc3NjEzNzAzMTgzMA.GwYNH1.9dCbPGiNEEtpzbiMxmyinM1dLX7jD1lmzOP1CE')




