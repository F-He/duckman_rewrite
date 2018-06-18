import discord
from src.embeds import EmbedGenerator
from discord.ext import commands
from src.secrets import BOT_TOKEN
from src.database import Database
from src.exceptions import UserNotFoundException
from src.levelSystem import LevelSystem
from src.utils import Utils

bot = commands.Bot(command_prefix='~')
bot.remove_command('help')

database = Database("grewoss", bot)

embedgenerator = EmbedGenerator(bot, database)

levelsystem = LevelSystem(database, embedgenerator)

duckUtils = Utils(database)


"""EVENTS"""
@bot.event
async def on_ready():
	await embedgenerator.load_embeds()
	for guild in bot.guilds:
		for channel in guild.channels:
			if isinstance(channel, discord.TextChannel):
				await database.create_channel(channel)
		for role in guild.roles:
			await database.create_role(role)
		for user in guild.members:
			if not await database.create_user(user):
				await database.update_user_roles(user)
	print("done")


@bot.event
async def on_member_join(member):
	await database.create_user(member)


@bot.event
async def on_member_remove(member):
	await database.delete_user_by_ID(member.id)


"""COMMANDS"""
@bot.event
async def on_message(message):
	await bot.process_commands(message)
	await levelsystem.add_to_user_xp(message.author.id, 2)
	level_message = await levelsystem.check_level(message.author)
	if level_message is not None:
		await message.channel.send(embed=level_message)
	await database.check_channel(message.author.id, message.channel.id)
	await database.detect_favorite_channel(message.author.id)


@bot.command()
@commands.guild_only()
async def vote(ctx, user: discord.Member):
	voter = ctx.message.author
	if await duckUtils.userIsElegibleToVote(voter.id):
		if voter.id == user.id:
			await ctx.send("You can't vote for yourself!")
		elif len(ctx.message.mentions) > 1:
			await ctx.send("You can only vote for 1 Person!")
		else:
			try:
				await database.user_voted_for(voter.id, user.id)
				await ctx.send(f"{voter.mention} voted successfully for {user.mention}")
			except UserNotFoundException as e:
				if e.user_id == voter.id:
					await database.create_user(voter)
					await database.user_voted_for(voter.id, user.id)
					await ctx.send(f"{voter.mention} voted successfully for {user.mention}")
				elif e.user_id == user.id:
					await database.create_user(user)
					await database.user_voted_for(voter.id, user.id)
					await ctx.send(f"{voter.mention} voted successfully for {user.mention}")
	else:
		await ctx.send("You can only vote once a week!")
@vote.error
async def vote_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send(f">>Please use an valid Argument.<<\n>>`{ctx.message.content}` is invalid!<<")


@bot.command(aliases=["?", "hilfe"])
async def help(ctx, *args):
	await ctx.send(embed=await embedgenerator.get_embed("help"))


@bot.command()
async def github(ctx):
	await ctx.send(embed=await embedgenerator.get_embed("github"))


@bot.command()
async def xp(ctx):
	await ctx.send(await levelsystem.get_user_xp(ctx.message.author.id))


@bot.command()
async def set_level(ctx, user, level):
	await levelsystem.set_user_level(ctx.message.mentions[0].id, level)
	await ctx.send("Level Set!")


@bot.command()
async def info(ctx, user: discord.Member = None):
	if user is not None:
		await ctx.send(embed=await embedgenerator.generateMeEmbed(user))
	else:
		await ctx.send(embed=await embedgenerator.generateMeEmbed(ctx.message.author))
@info.error
async def info_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send(f">>Please use an valid Argument.<<\n>>`{ctx.message.content}` is invalid!<<")

bot.run(BOT_TOKEN)