import discord
from src.embeds import EmbedGenerator
from discord.ext import commands
from src.secrets import BOT_TOKEN
from src.database import Database
from src.exceptions import UserNotFoundException

bot = commands.Bot(command_prefix='~')
bot.remove_command('help')

database = Database("grewoss")

embedgenerator = None


@bot.event
async def on_ready():
    global embedgenerator
    embedgenerator = EmbedGenerator(bot)
    guild_step = 100 / len(bot.guilds)
    guild_progress = 0
    for guild in bot.guilds:
        role_step = 100 / len(guild.roles)
        role_progress = 0
        member_step = 100 / len(guild.members)
        member_progress = 0

        for role in guild.roles:
            await database.create_role(role)
            role_progress += role_step
            print(f"Role Progress: {int(role_progress)}%")
        for user in guild.members:
            await database.create_user(user)
            member_progress += member_step
            print(f"Member Progress: {int(member_progress)}%")
        guild_progress += guild_step
        print(f"Guild Progress: {int(guild_progress)}%")
    print("done")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    await database.add_to_user_xp(message.author.id, 2)

@bot.command()
async def vote(ctx, arg1):
    if ctx.message.author.id == ctx.message.mentions[0].id:
        await ctx.send("You can't vote for yourself!")
    elif len(ctx.message.mentions) > 1:
        await ctx.send("You can only vote for 1 Person once a week!")
    else:
        try:
            await database.user_voted_for(ctx.message.author.id, ctx.message.mentions[0].id)
            await ctx.send(f"You voted successfully for {ctx.message.mentions[0].mention}")
        except UserNotFoundException as e:
            if e.user_id == ctx.message.author.id:
                await database.create_user(ctx.message.author)
                await database.user_voted_for(ctx.message.author.id, ctx.message.mentions[0].id)
                await ctx.send(f"You voted successfully for {ctx.message.mentions[0].mention}")
            elif e.user_id == ctx.message.mentions[0].id:
                await database.create_user(ctx.message.mentions[0])
                await database.user_voted_for(ctx.message.author.id, ctx.message.mentions[0].id)
                await ctx.send(f"You voted successfully for {ctx.message.mentions[0].mention}")



@bot.command(aliases=["?", "hilfe"])
async def help(ctx, *args):
    await ctx.send(embed=await embedgenerator.get_embed("help"))

@bot.command()
async def github(ctx):
    await ctx.send(embed=await embedgenerator.get_embed("github"))

@bot.command()
async def xp(ctx):
    await ctx.send(await database.get_user_xp(ctx.message.author.id))

bot.run(BOT_TOKEN)