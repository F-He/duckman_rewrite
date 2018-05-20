import discord
from src.embeds import EmbedGenerator
from discord.ext import commands
from src.secrets import BOT_TOKEN as TOKEN


bot = commands.Bot(command_prefix='~')
bot.remove_command('help')
embedgenerator = None


@bot.event
async def on_ready():
    print("Ready")
    global embedgenerator
    embedgenerator = EmbedGenerator(bot)

@bot.command()
async def help(ctx, *args):
    await ctx.send(embed=await embedgenerator.get_embed("help"))

@bot.command()
async def github(ctx):
    await ctx.send(embed=await embedgenerator.get_embed("github"))

bot.run(TOKEN)