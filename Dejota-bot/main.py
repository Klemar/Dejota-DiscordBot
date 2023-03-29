import discord
from discord.ext import commands
import os

#import bot token
from bot_token import *
client = commands.Bot(command_prefix = "!")

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

@client.command(name="sair")
async def sair(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Deixei o canal de voz')
    else:
        await ctx.send("Eu não estou em um canal de voz")

client.run(token)
