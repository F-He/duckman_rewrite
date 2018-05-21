import discord
import yaml

BOT_COLOR = 0x547e34

class EmbedGenerator(object):
	def __init__(self, bot):
		self._bot = bot
		self._embed_names = []
		self._all_embeds = {}


		self.generateEmbed("./embeds/help.yml", "help")
		self.generateEmbed("./embeds/github.yml", "github")
		

	def generateEmbed(self, path: str, name: str):
		"""
		Generate an Embed based on an YAML File.

		:path: The path to the YAML File.
		:name: The name to access the Embed later.
		:return: The generated Embed.
		"""
		with open(path, 'r', encoding='utf-8') as stream:
			gen_dict = yaml.load(stream, Loader=yaml.Loader)
		gen_dict = check_dict(gen_dict)
		
		gen_embed = discord.Embed(title=gen_dict["header"]["title"], description=gen_dict["header"]["description"], color=gen_dict["color"], url=gen_dict["header"]["url"])

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
	
	async def get_all_names(self):
		"""
		Gets the Names of all loaded Embeds.
		"""
		return self._embed_names


	async def get_embed(self, name: str):
		"""
		Get a embed by it's name.
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
	Checks for Keys inside the loaded dictonary and creates the missing one's to prevent KeyError's
	"""
	if "fields" not in _dict:
		_dict["fields"] = None
	if "footer" not in _dict:
		_dict["footer"] = None
	if "color" not in _dict:
		_dict["color"] = BOT_COLOR
	if "show_thumbnail" not in _dict:
		_dict["show_thumbnail"] = False
	return _dict


if __name__ == '__main__':
	selsdagadsfg = EmbedGenerator("bot")