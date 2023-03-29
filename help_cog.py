import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
Comandos Gerais:
!ajuda - Mostra todos os comandos
!tocar - Busca a música desejada do youtube e a reproduz
!fila - Mostra a seleção de músicas da atual fila
!proxima - Passa para proxima música da fila
!limpar - Para a música e limpa a fila
!sair - Desconecta o bot do canal de voz
!pausar - Pausa a música que esta tocando
!continuar - Continua a tocar a fila que havia sido pausada
```
"""        

    @commands.command(name="ajuda", aliases=["a", "h"], help="Mostra todos os comandos")
    async def ajuda(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)