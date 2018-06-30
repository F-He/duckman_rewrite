import discord
import json
from src.database import Database
from src.role import RoleManager

BOT_COLOR = 0x547e34

class EmbedGenerator(object):
	def __init__(self, bot, database: Database, roleManager: RoleManager):
		self._bot = bot
		self._database = database
		self._roleManager = roleManager
		self._embed_names = []
		self._all_embeds = {}

	async def load_embeds(self):
		self.generateEmbed("./embeds/help.json", "help")
		self.generateEmbed("./embeds/github.json", "github")
		self.generateEmbed("./embeds/welcome.json", "welcome")
		
	def generateEmbed(self, path: str, name: str):
		"""
		Generate an embed based on a JSON File.

		:param path: The path to the JSON File.
		:param name: The name to access the Embed later.
		:return: The generated Embed.
		"""
		with open(path, 'r', encoding="utf-8") as stream:
			gen_dict = json.load(stream)
		gen_dict = check_dict(gen_dict)
		
		gen_embed = discord.Embed(title=gen_dict["header"]["title"], url=gen_dict["header"]["url"])
		gen_embed.colour = int(gen_dict["color"], 16)
		
		if gen_dict["header"]["description"] is not None:
			gen_embed.description = gen_dict["header"]["description"]
		if gen_dict["header"]["url"] is not None:
			gen_embed.url = gen_dict["header"]["url"]
		if gen_dict["fields"] is not None:
			for field, content in gen_dict["fields"].items():
				gen_embed.add_field(name=content["title"], value=content["description"])
		if gen_dict["footer"] is not None:
			gen_embed.set_footer(text=gen_dict["footer"])
		if gen_dict["show_thumbnail"]:
			gen_embed.set_thumbnail(url=self._bot.user.avatar_url)

		self._embed_names.append(name)
		self._all_embeds[name] = gen_embed
		return gen_embed
	
	async def generateLevelEmbed(self, user: discord.Member, level: int, value: dict):
		gen_embed = discord.Embed(title="Level Up!!", description="{} is now Level {}!".format(user.name, level), color=BOT_COLOR)
		if value["rewards"] is not None:
			gen_embed.add_field(name="Rewards", value=value["rewards"])
		return gen_embed
	
	async def generateMeEmbed(self, user: discord.Member):
		databaseUser = await self._database.find_user(user.id)
		gen_embed = discord.Embed(title=f"Info's about {user.name}", color=BOT_COLOR)
		gen_embed.add_field(name="XP:", value=databaseUser.xp, inline=True)
		gen_embed.add_field(name="Level:", value=databaseUser.level, inline=True)
		gen_embed.add_field(name="Current Votes:", value=databaseUser.helper_votes, inline= True)
		gen_embed.add_field(name="Currency:", value=databaseUser.currency, inline=True)
		gen_embed.add_field(name="Favorite Channel:", value=databaseUser.fav_channel, inline=True)
		gen_embed.set_thumbnail(url=user.avatar_url)
		return gen_embed
	
	async def generateRoleEmbed(self, user: discord.Member):
		availableRoles = await self._roleManager.getAvailableRoles()
		gen_embed = discord.Embed(title=f"Role Managment - {user.name}", description="Manage your roles here!", color=BOT_COLOR)

		content = ""
		for role in user.roles:
			if role.name in availableRoles["languages"].values():
				content += f"-{role.name}\n"
		if not content:
			content += "No roles found."
		gen_embed.add_field(name="Current Roles", value=content)
		gen_embed.add_field(name="Options", value="➕ Add new Roles/Skills\n➖ Remove Roles\n🚮 Remove all Roles", inline=False)
		return gen_embed
	
	async def generateAddRoleEmbed(self, user: discord.Member):
		pass
	
	async def generateRemoveRoleEmbed(self, user: discord.Member):
		availableRoles = await self._roleManager.getAvailableRoles()
		gen_embed = discord.Embed(title=f"Remove Roles - {user.name}", color=BOT_COLOR)

		content = ""
		for emoji, rolename in availableRoles["languages"].items():
			role = discord.utils.get(user.roles, name=rolename)
			if role is not None:
				content += f"{emoji} {role}\n"
		if not content:
			content += "No roles found."
		gen_embed.description = content
		return gen_embed
	
	async def generateRemoveAllRolesEmbed(self, user: discord.Member):
		gen_embed = discord.Embed(title=f"Remove Roles - {user.name}", description="All Roles removed!", color=BOT_COLOR)
		return gen_embed
	
	async def get_all_names(self):
		"""
		Gets the names of all loaded embeds.
		"""
		return self._embed_names

	async def get_embed(self, name: str):
		"""
		Get a embed by its name.
		:return: Returns the Embed. None if Embed not found!
		"""
		try:
			return self._all_embeds[name]
		except KeyError:
			return None
	
	async def get_all_embed(self):
		"""
		Get all loaded embeds.
		"""
		return self._all_embeds


def check_dict(_dict: dict):
	"""
	Checks for keys inside the loaded dictionary and creates the missing ones to prevent key errors.
	"""
	if "fields" not in _dict:
		_dict["fields"] = None
	if "footer" not in _dict:
		_dict["footer"] = None
	if "color" not in _dict:
		_dict["color"] = str(BOT_COLOR)
	if "show_thumbnail" not in _dict:
		_dict["show_thumbnail"] = False
	return _dict


if __name__ == '__main__':
	pass
