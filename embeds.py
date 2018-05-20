import discord
import yaml

BOT_COLOR = 0x547e34

class EmbedGenerator(object):
	def __init__(self, bot):
		self._bot = bot
		self._embed_names = []
		self._all_embeds = {}

		self.generateEmbed("embeds/help.yml", "help")
		

	def generateEmbed(self, path: str, name: str):
		with open(path, 'r', encoding='utf-8') as stream:
			gen_dict = yaml.load(stream, Loader=yaml.Loader)

		if "color" not in gen_dict:
			gen_dict["color"] = BOT_COLOR
		
		gen_embed = discord.Embed(title=gen_dict["header"]["title"], color=gen_dict["color"], url=gen_dict["header"]["url"])
		for field, content in gen_dict["fields"].items():
			gen_embed.add_field(name=content["title"], value=content["description"])
		gen_embed.set_footer(text=gen_dict["footer"])
		gen_embed.set_thumbnail(url=self._bot.user.avatar_url)

		self._embed_names.append(name)
		self._all_embeds[name] = gen_embed
	
	async def get_all_names(self):
		return self._embed_names


	async def get_embed(self, name: str):
		try:
			return self._all_embeds[name]
		except KeyError:
			return None
	
	
	async def get_all_embed(self):
		return self._all_embeds



if __name__ == '__main__':
	selsdagadsfg = EmbedGenerator("bot")