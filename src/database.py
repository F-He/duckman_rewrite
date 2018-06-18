from py2neo import Node, Graph, Relationship
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from src.exceptions import UserNotFoundException
import discord
import time
import ast
import operator


class Channel(GraphObject):
	__primarykey__ = "id"

	id = Property()
	name = Property()
	total_messages = Property()

	users = RelatedFrom("User", "ISFAVORITE")


class Role(GraphObject):
	__primarykey__ = "id"

	id = Property()
	name = Property()

	users = RelatedFrom("User", "HAS")


class User(GraphObject):
	__primarykey__ = "id"

	id = Property()
	name = Property()
	level = Property()
	xp = Property()
	helper_votes = Property()
	last_vote_made_on = Property()
	currency = Property()
	channels = Property()
	fav_channel = Property()

	roles = RelatedTo("Role", "HAS")
	voted_for = RelatedTo("User", "VOTED")
	favorite_channel = RelatedTo("Channel", "ISFAVORITE")

	got_vote_from = RelatedFrom("User", "VOTED")


class Database(object):
	def __init__(self, password: str, bot):
		self._graph = Graph("bolt://localhost:7687", password=password)
		self._bot = bot
		print(self._graph)
	

	async def create_user(self, discord_user: discord.User):
		"""
		Returns True if a new user has been created.
		Else False
		"""
		if User.select(self._graph, discord_user.id).first() is None:
			user = User()
			user.id = discord_user.id
			user.name = discord_user.name
			user.level = 0
			user.xp = 0
			user.helper_votes = 0
			user.last_vote_made_on = None
			user.currency = 0
			user.fav_channel = None
			user.channels = str({})

			user = await self.role_update_loop(discord_user, user)
			
			self._graph.push(user)
			return True
		return False
	
	async def create_role(self, _role: discord.Role):
		if Role.select(self._graph, _role.id).first() is None:
			role = Role()
			role.id = _role.id
			role.name = _role.name
			
			self._graph.push(role)
	
	async def create_channel(self, _channel: discord.TextChannel):
		if Channel.select(self._graph, _channel.id).first() is None:
			channel = Channel()
			channel.id = _channel.id
			channel.name = _channel.name

			channel.total_messages = 0

			self._graph.push(channel)
	
	async def find_user(self, _user_id: int, selfcall: bool = False):
		"""
		Use this to find a User by it's id.
		Throws a UserNotFoundException if user can't be found.
		:return: User Object see database.py User(GraphObject) class.
		"""
		user = User.select(self._graph, _user_id).first()
		if user is not None:
			return user
		else:
			discord_user = self._bot.get_user(_user_id)
			if discord_user is not None:
				if await self.create_user(discord_user) and not selfcall:
					return await self.find_user(_user_id, True)
				else:
					raise UserNotFoundException(_user_id)
			else:
				raise UserNotFoundException(_user_id)
	
	async def find_channel(self, _channel_id):
		channel = Channel.select(self._graph, _channel_id).first()
		if channel is not None:
			return channel
		else:
			return None

	
	async def update_user(self, user: User):
		self._graph.push(user)
	
	async def delete_user_by_ID(self, _user_id: int):
		user = self.find_user(_user_id)
		self._graph.delete(user)
	
	async def update_user_roles(self, discord_user: discord.Member):
		raw_user = await self.find_user(discord_user.id)
		user = await self.role_update_loop(discord_user, raw_user)
		await self.update_user(user)
	
	async def role_update_loop(self, discord_user: discord.Member, user: User):
		"""
		Loops trough every role and links it inside the database.
		:param :
		:returns: A Database User Object
		"""
		for _role in discord_user.roles:
				if not _role.is_default():
					new_role = Role.select(self._graph, _role.id).first()
					user.roles.add(new_role)
		return user

	async def get_user_xp(self, _user_id: int):
		user = await self.find_user(_user_id)
		return user.xp

	async def add_to_user_xp(self, _user_id:int, xp_to_add: int):
		user = await self.find_user(_user_id)
		user.xp = user.xp + xp_to_add
		await self.update_user(user)
	
	async def get_user_level(self, _user_id: int):
		user = await self.find_user(_user_id)
		if user.level is None:
			await self.set_user_level(_user_id, 0)
			return 0
		return int(user.level)
	
	async def set_user_level(self, _user_id: int, new_level: int):
		user = await self.find_user(_user_id)
		user.level = new_level
		await self.update_user(user)
	
	async def user_voted_for(self, _user_who_voted_id: int, _user_who_got_voted_id: int):
		user_who_voted = await self.find_user(_user_who_voted_id)
		user_who_got_voted = await self.find_user(_user_who_got_voted_id)
		user_who_got_voted.helper_votes += user_who_got_voted.helper_votes + 1
		user_who_voted.voted_for.add(user_who_got_voted)
		await self.update_user(user_who_voted)
		await self.set_last_vote_time_to_now(_user_who_voted_id)
	
	async def get_last_vote_time(self, _user_id: int):
		user = await self.find_user(_user_id)
		return user.last_vote_made_on
	
	async def set_last_vote_time_to_now(self, _user_id: int):
		user = await self.find_user(_user_id)
		user.last_vote_made_on = time.time()
		await self.update_user(user)
	
	async def get_currency(self, _user_id: int):
		user = await self.find_user(_user_id)
		return user.currency
	
	async def set_currency(self, _user_id: int, new_currency_amount: int):
		user = await self.find_user(_user_id)
		user.currency = new_currency_amount
		await self.update_user(user)
	
	async def add_currency(self, _user_id: int, currency_to_add: int):
		user = await self.find_user(_user_id)
		user.currency = user.currency + currency_to_add
		await self.update_user(user)
	
	async def check_channel(self, _user_id: int, _channel_id: int):
		user = await self.find_user(_user_id)
		temporaryDictionary = ast.literal_eval(user.channels)
		try:
			value = temporaryDictionary[_channel_id]
			temporaryDictionary[_channel_id] = value + 1
		except KeyError:
			temporaryDictionary[_channel_id] = 0
		finally:
			user.channels = str(temporaryDictionary)
			await self.update_user(user)
	
	async def detect_favorite_channel(self, _user_id: int):
		user = await self.find_user(_user_id)
		channel = await self.get_favorite_channel(_user_id)
		if channel is not None:
			user.fav_channel = channel.name
			user.favorite_channel.clear()
			user.favorite_channel.add(channel)
			await self.update_user(user)
	
	async def get_favorite_channel(self, _user_id: int):
		user = await self.find_user(_user_id)
		channelDictionary = ast.literal_eval(user.channels)
		favorite_channel_id = max(channelDictionary.items(), key=operator.itemgetter(1))[0]
		channel = await self.find_channel(favorite_channel_id)
		return channel
