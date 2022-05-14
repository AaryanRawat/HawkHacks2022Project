import discord
import asyncio
import streetview as sv
import os

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

playlists = ['Romantic Movie Locations', 'Horror Movie Locations', 'Random Movie Locations']
playlists_check = ['Romantic', 'Horror', 'Random']

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('geodude-hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('geodude-commands'):
        await message.channel.send('geodude-hello')
        await message.channel.send('geodude-commands')
        await message.channel.send('geodude-start')

    if message.content.startswith('geodude-start'):
        await message.channel.send('Select A Playlist: ')
        await message.channel.send(f'1. {playlists[0]} : ')
        await message.channel.send(f'2. {playlists[1]}: ')
        await message.channel.send(f'3. {playlists[2]}: ')
        await message.channel.send('Type out the first word of playlist name, For eg. Romantic for Romantic Movie Locations')
        def check(msg):
            for item in playlists_check:
                if(msg == item):
                    return True
        try:
            msg = await client.wait_for("message", check = check, timeout = 30)
            #start of the game where we need the google api stuff. probably need a class to store all the pulled data
            #and do comparisons with user answers. 
            await message.channel.send(f'You selected {msg} playlist!')

        except asyncio.TimeoutError:
            await message.channel.send('Selection took too long, please try again')

client.run(os.getenv('TOKEN'))