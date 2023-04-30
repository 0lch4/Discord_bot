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


piekna_ola=['kto jest najpiekniejszy na swiecie?',
            'kto jest najpiekniejszy na swiecie',
            'kto jest najpiękniejszy na świecie?',
            'kto jest najpiękniejszy na świecie',
            'kto jest najpiekniejszy na świecie?',
            'kto jest najpiekniejszy na świecie',
            'kto jest najpiękniejszy na swiecie?'
            'kto jest najpiękniejszy na swiecie'
            ]
powitanie=['hej','czesc','siema','witaj','cześć','elo','hejka']
olchus = ['olchus','olchuś']

@bot.event
async def on_ready():
    print(f'Witaj mój stwórco to ja {bot.user} jestem gotów by ci służyć')


@bot.command(name='test')
async def hello(ctx):
    await ctx.send('test')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(message.content.lower().startswith(p) for p in powitanie) and any(o in message.content.lower() for o in olchus):
        await message.channel.send(random.choice(powitanie))
    if any(i in message.content.lower() for i in piekna_ola):
        await message.channel.send('Proste, że Olusia <3')
        
    if message.content.lower().startswith(tuple(f'{i} włącz ' for i in olchus)):
        nuta = message.content.lower().split('włącz ')[1]
        results = sp.search(q=nuta, limit=1, type='track')
        if len(results['tracks']['items']) > 0:
                track_uri = results['tracks']['items'][0]['uri']
                audio_url = sp.track(track_uri)['preview_url']
                await message.channel.send('no pewnie')
                channel = message.author.voice.channel
                vc = await channel.connect(reconnect=True, timeout=10.0)
                vc.play(FFmpegPCMAudio(audio_url+"&play=true", executable="ffmpeg.exe", options="-vn"))
        else:
                await message.channel.send("nie widze takiej")
    
    if message.content.lower().startswith(tuple(f'{i} poleć coś podobnego do ' for i in olchus)):
        tytul = message.content.lower().split('poleć coś podobnego do ')[1]
        
        with open('wynik2.json','r',encoding='utf-8') as f:
            czy_jest = json.load(f)
            
        with open('wynik.json','w',encoding='utf-8') as f:
            json.dump(tytul,f, indent=2, ensure_ascii=False)       
        subprocess.run(["python", "C:\Repositories\discord_bot\polecenie_muzyki\pobranie_piosenki.py"])
        
        with open('wynik2.json','r',encoding='utf-8') as f:
            czy_jest_nowe = json.load(f)
            
        if czy_jest == czy_jest_nowe:
            await message.channel.send("zla nute podales sprobuj znowu i daj sam tytul")
        else:
            await message.channel.send("dobra mysle czaj")
            subprocess.run(["python", "C:\Repositories\discord_bot\polecenie_muzyki\AI.py"])
            await message.channel.send("dobra a gatunek jaki chcesz miec? masz do wyboru:")
            with open('polecenie_muzyki\gatunki.txt') as f:
                for gatunek in f:
                    await message.channel.send(gatunek)
                                        
            user_message = await bot.wait_for('message', check=lambda m: m.author == message.author)
            with open('polecenie_muzyki\gatunek.json','w') as f:
                json.dump(user_message.content,f, indent=2, ensure_ascii=False)
                
            subprocess.run(["python", "C:\Repositories\discord_bot\polecenie_muzyki\zwrócenie_piosenki.py"])
            with open('wynik4.json','r',encoding='utf-8') as f:
                polecane = json.load(f)
                miejsce = 1
            for polecenie in polecane:
                tytul = polecenie['utwór']
                wykonawca = polecenie['wykonawca']
                link = polecenie['link']
                await message.channel.send(f"Miejsce: {miejsce}\n{tytul} - {wykonawca}\n{link}")
                miejsce+=1
                
    
    await bot.process_commands(message)
    

bot.run('MTEwMTQ3MTc3NjEzNzAzMTgzMA.GwYNH1.9dCbPGiNEEtpzbiMxmyinM1dLX7jD1lmzOP1CE')




