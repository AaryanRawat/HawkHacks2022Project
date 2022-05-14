import discord
import asyncio
import streetview as sv
import os

from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True

playlists = ['Romantic Movie Locations', 'Horror Movie Locations', 'Random Movie Locations']
playlists_check = ['Romantic', 'Horror', 'Random']

bot = commands.Bot('geodude ')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def commands(ctx):
    comms = ['hello', 'commands', 'start']
    await ctx.send((f'{com}' for com in enumerate(comms)) + '\n')

@bot.command()
async def start(ctx):
    await ctx.send(
        'Select A Playlist:\n'
        + '\n'.join(f'{i+1}. {playlist}' for i, playlist in enumerate(playlists)) +
        '\nType out the first word of playlist name, For eg. Romantic for Romantic Movie Locations'
    )
    def check(msg):
        if msg.author == ctx.author:
            return any(msg.content == playlist for playlist in playlists_check)
        return False
    try:
        msg = await bot.wait_for("message", check = check, timeout = 30)
        #start of the game where we need the google api stuff. probably need a class to store all the pulled data
        #and do comparisons
        await ctx.send(f'You selected {msg.content} playlist!')

    except asyncio.TimeoutError:
        await ctx.channel.send('Selection took too long, please try again')

bot.run('OTc0ODUzMjc2OTIxMTM1MTA0.G9CYa8.BBkD6vwHez-zU8s9TO4onrBXyUgzLqTA4VCZJg')