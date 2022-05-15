import discord
import asyncio
import streetview as sv
import os
import playlists
import random
from envreader import ENV

from discord.ext import commands

NUMBER_OF_ROUNDS = 5
SV = sv.StreetView(key=ENV.get('API_KEY'), dest='images')

intents = discord.Intents.default()
intents.messages = True

#PLAYLISTS = ['Capital cities of the world', 'Horror Movie Locations', 'Landmarks of the world']
PLAYLISTS = [
    playlists.Playlist('data/capitals.xlsx', 'Capital Cities of the World'),
    playlists.Playlist('data/horror_movies.xlsx', 'Horror Movie Locations'),
    playlists.Playlist('data/landmarks.xlsx', 'Landmarks of the world')
]
PLAYLISTS_CHECK = [playlist.name.split()[0] for playlist in PLAYLISTS]

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
    await ctx.send((f'{com}' for com in enumerate(comms)))


@bot.command()
async def start(ctx):
    await ctx.send(
        'Select A Playlist:\n' +
        '\n'.join(f'{i+1}. {playlist.name}'
                  for i, playlist in enumerate(PLAYLISTS)) +
        '\nType out the first word of playlist name, For eg. Capital for Capital Cities of the World'
    )

    def check(msg):
        if msg.author == ctx.author:
            return any(msg.content == playlist.name.split()[0]
                       for playlist in PLAYLISTS)
        return False

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        #start of the game where we need the google api stuff. probably need a class to store all the pulled data
        #and do comparisons
        await ctx.send(f'You selected {msg.content} playlist!')
        for playlist in PLAYLISTS:
            if (msg.content == playlist.name.split()[0]):
                await ctx.send('Valid Playlist Selected!')
                gameRound = 1
                gameLocations = random.sample(playlist.locations,
                                              k=NUMBER_OF_ROUNDS)
                print(gameLocations)

                points = 0

                for gameLocation in gameLocations:
                    SV.saveLocationDefault(gameLocation['location'])

                    #question = gameLocation[
                    #    'movie']  # TODO Placeholder until we figure out how to write the question (hints for special categories?)

                    def validLocation(m):
                        print(SV.getCoordinates(m.content))
                        return SV.getCoordinates(
                            m.content) is not None and msg.author == ctx.author

                    await ctx.send(file=discord.File('images/gsv_0.jpg'))
                    await ctx.send("Where do you think this is?")
                    guess = await bot.wait_for("message", check=validLocation)
                    if msg.content == 'Horror':
                        await ctx.send("What movie do you think this is?")
                        ans_movie = await bot.wait_for(
                            "message",
                            check=lambda msg: msg.author == ctx.author)
                    elif msg.content == 'Landmarks':
                        await ctx.send(
                            "What famous landmark do you think this is?")
                        ans_landmark = await bot.wait_for(
                            "message",
                            check=lambda msg: msg.author == ctx.author)

                    ans = SV.getCurrentCoordinates()
                    guess = SV.getCoordinates(guess.content)
                    pts = playlists.points(ans['lat'], ans['lng'],
                                           guess['lat'], guess['lng'])
                    points += pts
                    await ctx.send(content="The answer is " +
                                   gameLocation['location'] + ", in " +
                                   SV.getAddress(gameLocation['location']) +
                                   ". You gained " + str(pts) + " points.")

                    if msg.content == 'Horror':
                        if (ans_movie.content.lower()
                                in gameLocation['movie'].lower()):
                            pts = 500
                        else:
                            pts = 0
                        points += pts
                        await ctx.send(content="The movie was " +
                                       gameLocation['movie'] +
                                       ". You earned " + str(pts) + " points.")
                    elif msg.content == 'Landmarks':
                        if (ans_landmark.content.lower()
                                in gameLocation['location'].lower()):
                            pts = 500
                        else:
                            pts = 0
                        points += pts
                        await ctx.send(content="The landmark was " +
                                       gameLocation['location'] +
                                       ". You earned " + str(pts) + " points.")
                await ctx.send(content="Congratuations, you earned " +
                               str(points) + " total points!")

    except asyncio.TimeoutError:
        await ctx.send('Selection took too long, please try again')

    # TODO Implement gameplay
    #- Load playlist
    #- Select locations from playlist
    # Loop through locations, playing the game
    # For each location:
    #   Send photo with question
    #   Await response
    #   Process response, calculate distance => score
    #   Return score
    # Return "Your total score was {score} \n Use <geodude start> command to play again"


bot.run(ENV.get('BOT_KEY'))