from ast import alias
import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Não foi possível conectar um canal de voz")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="tocar", aliases=["p", "play"],  help="Busca a música desejada do youtube e a reproduz")
    async def tocar(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Entrei no canal de voz!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Não foi possível encontrar a música. Formato incorreto tente outra palavra-chave. Isso pode ser devido à lista de reprodução ou a um formato de transmissão ao vivo")
            else:
                await ctx.send("Música adicionada a fila")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pausar", aliases=["pa", "pause"], help="Pausa a música que esta tocando")
    async def pausar(self, ctx, *args):

        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()

        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="continuar", aliases=["r", "resumem", "c"], help="Continua a tocar a fila que havia sido pausada")
    async def continuar(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="proxima", aliases=["skip", "pr"], help="Passa para proxima música da fila")
    async def proxima(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="fila", aliases=["f", "queue", "q"], help="Mostra a seleção de músicas da atual fila")
    async def fila(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Sem músicas na fila")

    @commands.command(name="limpar", aliases=["bin", "clean", "l"], help="Para a música e limpa a fila")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Fila limpa")

    @commands.command(name="sair", aliases=["disconnect", "leave", "s"], help="Desconecta o bot do canal de voz")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
