import discord
from discord.ext import commands
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

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

    if any(message.content.lower().startswith(p) for p in powitanie) and any(message.content.lower() for o in olchus):
        await message.channel.send(random.choice(powitanie))
    if any(i in message.content.lower() for i in piekna_ola):
        await message.channel.send('Proste, że Olusia <3')

    await bot.process_commands(message)

bot.run('MTEwMTQ3MTc3NjEzNzAzMTgzMA.GwYNH1.9dCbPGiNEEtpzbiMxmyinM1dLX7jD1lmzOP1CE')