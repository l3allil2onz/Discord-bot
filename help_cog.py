import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text_channel_text = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

    @commands.command(name="คำสั่ง",help="แสดงคำสั่งทั้งหมดที่มี")
    async def help(self, ctx):
        self.help_message = "⚙️ คำสั่ง:"+ """
```
    /คำสั่ง - แสดงคำสั่งทั้งหมดที่มี

# หมวดเพลง 🎵
    /เล่น <ชื่อเพลง> - ค้นหาเพลงบนยูทูป และเริ่มเล่นเพลงที่แชแนลปัจจุบันที่คุณอยู่
    /คิว - แสดงคิวเพลงทั้งหมด
    /ข้าม - ข้ามเพลงปัจจุบันที่กำลังเล่นอยู่
    /ล้างคิว - ล้างคิวเพลง และหยุดเพลงที่กำลังเล่น
    /ปิด - ตัดการเชื่อมต่อบอทออกจากแชท
    /หยุด - หยุดเพลงปัจจุบันที่กำลังเล่น หรือ เล่นเพลงปัจจุบันต่อ หากถูกหยุดไว้แล้ว
    /เล่นต่อ - เล่นเพลงปัจจุบันต่อหากถูกหยุด
```
"""
        await ctx.send(self.help_message)