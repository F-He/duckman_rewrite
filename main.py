import discord
from embeds import EmbedGenerator
from discord.ext import commands
from secrets import BOT_TOKEN as TOKEN


bot = commands.Bot(command_prefix='~')
bot.remove_command('help')
embedgenerator = None


@bot.event
async def on_ready():
    print("Ready")
    global embedgenerator
    embedgenerator = EmbedGenerator(bot)

@bot.command()
async def help(ctx):
    await ctx.send(embed=await embedgenerator.get_embed("help"))

bot.run(TOKEN)