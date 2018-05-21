import discord
from src.embeds import EmbedGenerator
from discord.ext import commands
from src.secrets import *
from src.database import Database


bot = commands.Bot(command_prefix='~')
bot.remove_command('help')

database = Database(MONGO_DB_KEY)

embedgenerator = None


@bot.event
async def on_ready():
    print("Ready")
    global embedgenerator
    embedgenerator = EmbedGenerator(bot)

@bot.command(aliases=["?", "hilfe"])
async def help(ctx, *args):
    await ctx.send(embed=await embedgenerator.get_embed("help"))

@bot.command()
async def github(ctx):
    await ctx.send(embed=await embedgenerator.get_embed("github"))

@bot.command()
async def xp(ctx):
    await ctx.send("Du hast: {}".format(await database.get_user_xp(ctx.message.author.id)))

bot.run(BOT_TOKEN)