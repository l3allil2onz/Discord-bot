import discord
from discord.ext import commands
from help_cog import help_cog
from music_cog import music_cog

token = 'MTEyODQzMDI4Njc2MjQxNDIyMA.GGa6Ar.OV4Bo0ejRE--rTnBx9e6LS4C3MMcPpt988drE0'
bot = commands.Bot(command_prefix='/')

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

@bot.event
async def on_ready() :
    print("The Tippawan bot has been started!")

@bot.event
async def on_member_join(member):
    print (f"<@!{member.name}> has joined")
    await member.send(f"<@!{member.name}> has joined")

@bot.command()
async def ping(ctx) :
    await ctx.send(ctx.message.author.mention)

bot.run(token)