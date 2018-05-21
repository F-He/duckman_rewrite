import discord
from src.embeds import EmbedGenerator
from discord.ext import commands
from src.secrets import *
from src.database import Database

bot = commands.Bot(command_prefix='~')
bot.remove_command('help')

database = Database("grewoss")

embedgenerator = None


@bot.event
async def on_ready():
    global embedgenerator
    embedgenerator = EmbedGenerator(bot)
    for guild in bot.guilds:
        for role in guild.roles:
            await database.create_role(role.name, role.id)
        for user in guild.members:
            await database.create_user(user)
    print("done")


@bot.command(aliases=["?", "hilfe"])
async def help(ctx, *args):
    await ctx.send(embed=await embedgenerator.get_embed("help"))

@bot.command()
async def github(ctx):
    await ctx.send(embed=await embedgenerator.get_embed("github"))

@bot.command()
async def xp(ctx):
    await ctx.send(await database.find_user(ctx.message.author.id))

bot.run(BOT_TOKEN)