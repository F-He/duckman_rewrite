from py2neo import Node, Graph, Relationship
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from src.exceptions import UserNotFoundException
import discord
import datetime


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

    roles = RelatedTo("Role", "HAS")
    voted_for = RelatedTo("User", "VOTED")

    got_vote_from = RelatedFrom("User", "VOTED")


class Database(object):
    def __init__(self, password: str):
        self.graph = Graph("bolt://localhost:7687", password=password)
        print(self.graph)
    

    async def create_user(self, discord_user: discord.Member):
        """
        Returns True if a new user has been created.
        Else False
        """
        if User.select(self.graph, discord_user.id).first() is None:
            user = User()
            user.id = discord_user.id
            user.name = discord_user.name
            user.level = 0
            user.xp = 0
            user.helper_votes = 0
            user.last_vote_made_on = None

            user = await self.role_update_loop(discord_user, user)
            
            self.graph.push(user)
            return True
    
    async def create_role(self, _role: discord.Role):
        if Role.select(self.graph, _role.id).first() is None:
            role = Role()
            role.id = _role.id
            role.name = _role.name
            
            self.graph.push(role)
    
    async def find_user(self, _user_id: int):
        """
        Use this to find a User by it's id.
        Throws a UserNotFoundException if user can't be found.
        :return: User Object see database.py User(GraphObject) class.
        """
        user = User.select(self.graph, _user_id).first()
        if user is not None:
            return user
        else:
            raise UserNotFoundException(_user_id)
    
    async def update_user(self, user: User):
        self.graph.push(user)
    
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
                    new_role = Role.select(self.graph, _role.id).first()
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
    
    async def get_last_vote_time(self, _user_id: int):
        user = await self.find_user(_user_id)
        return user.last_vote_made_on
    
    async def set_last_vote_time_to_now(self, _user_id: int):
        user = await self.find_user(_user_id)
        user.last_vote_made_on = datetime.datetime.utcnow()
        await self.update_user(user)