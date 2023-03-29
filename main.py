import discord
from discord.ext import commands
import os

#import client token
from bot_token import *

from help_cog import help_cog
from music_cog import music_cog

client = commands.Bot(command_prefix = "!")

client.remove_command('ajuda')

client.add_cog(help_cog(client))
client.add_cog(music_cog(client))

@client.event
async def on_ready():
    print('{0.user} ta na area'.format(client))

@client.command(name="oi")
async def oi(ctx):
    await ctx.send("Olá")

@client.command(name="criador")
async def criador(ctx):
    await ctx.send("Eu fui programado em python por João Pedro Klemar Covos")

@client.command(name="entrar")
async def entrar(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel   
        await channel.connect()
    else:
        await ctx.send("Você não esta em um canal de voz, entre em um canal de voz para usar este comando!")

client.run(token)
