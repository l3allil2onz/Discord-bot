import discord
from ast import alias
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
            return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                         after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("⚠️ ไม่สามารถเข้าสู่แชแนลได้")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                        after=lambda e: self.play_next())
            
        else:
            self.is_playing = False

    @commands.command(name="เล่น", aliases=["p", "playing"], help="เล่นเพลงที่ถูกเลือกจากยูทูป")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("⚠️ "+ctx.message.author.mention+" กรุณาเข้าแชแนลก่อน")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("⚠️ ไม่สามารถโหลดเพลงได้ เนื่องจากรูปแบบไม่ถูกต้อง, กรุณาลองค้นหาด้วยคีย์เวิร์ดอื่น" + """
```
[*] อาจเป็นเพราะเพลย์ลิสต์หรือรูปแบบสตรีมสด
[*] วีดีโออาจไม่สามารถเข้าถึงได้ เช่นข้อจำกัดทางภูมิภาค
```
""")
            else:
                await ctx.send("""```📥 เพลงได้ถูกเพิ่มในคิว```""")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="หยุด", help="หยุดเพลงปัจจุบันที่กำลังเล่น หรือ เล่นเพลงปัจจุบันต่อ หากถูกหยุดไว้แล้ว")
    async def pause(self):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="เล่นต่อ", aliases=["r"], help="เล่นเพลงปัจจุบันต่อหากถูกหยุด")
    async def resume(self):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="ข้าม", aliases=["s"], help="ข้ามเพลงปัจจุบันที่กำลังเล่นอยู่")
    async def resume(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            await ctx.send("""```ข้ามเพลง```""")
            await self.play_music(ctx)

    @commands.command(name="คิว", aliases=["q"], help="แสดงคิวเพลงทั้งหมด")
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            quote_text = '🗃️ คิว :\n>>> {}'.format(retval)
            await ctx.send(quote_text)
        else:
            await ctx.send("""```ไม่มีคิวเพลง```""")

    @commands.command(name="ล้างคิว", aliases=["c, bin"], help="ล้างคิวเพลง และหยุดเพลงที่กำลังเล่น")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("""```📤 คิวเพลงถูกล้าง```""")

    @commands.command(name="ปิด", aliases=["l, d, disconnected"], help="ตัดการเชื่อมต่อบอทออกจากแชท")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await ctx.send("""```🔌 ตัดการเชื่อมต่อบอท```""")
        await self.vc.disconnect()