from py2neo import Node, Graph, Relationship
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
import discord


class Role(GraphObject):
    __primarykey__ = "id"

    id = Property()
    name = Property()

    users = RelatedFrom("User", "HAS")


class User(GraphObject):
    __primarykey__ = "id"

    id = Property()
    name = Property()
    levels = Property()
    xp = Property()
    helper_votes = Property()
    last_vote_made_on = Property()

    roles = RelatedTo("Role", "HAS")


class Database(object):
    def __init__(self, password: str):
        self.graph = Graph("bolt://localhost:7687", password=password)
        print(self.graph)
    

    async def create_user(self, discord_user: discord.Member):
        if User.select(self.graph, discord_user.id).first() is None:
            user = User()
            user.id = discord_user.id
            user.name = discord_user.name
            user.levels = 0
            user.xp = 0
            user.helper_votes = 0
            user.last_vote_made_on = None

            for _role in discord_user.roles:
                new_role = Role.select(self.graph, _role.id).first()
                user.roles.add(new_role)
            
            self.graph.push(user)
    
    async def create_role(self, role_name: str, role_id: int):
        if Role.select(self.graph, role_id).first() is None:
            role = Role()
            role.id = role_id
            role.name = role_name
            
            self.graph.push(role)
    
    async def find_user(self, _user_id: int):
        user = User.select(self.graph, _user_id).first()
        print(user.xp)
        print(user.levels)
        return user
    
    # async def connect_user_to_role(self, discord_id: int, role_id: int):
    #     user_node = self.graph.find("User", "discord_id", discord_id)
    #     role_node = self.graph.find("Role", "role_id", role_id)
    #     relationship = Relationship(user_node, "HAS", role_node)
    #     self.graph.create(relationship)

# class Database(object):
#     def __init__(self, password: str):
#         self.graph = Graph("bolt://localhost:7687", password=password)
#         print(self.graph)
    

#     async def create_user(self, discord_id: int, user_name: str):
#         node = Node("User")
#         node["discord_id"] = discord_id
#         node["name"] = user_name
#         node["level"] = 0
#         node["xp"] = 0
#         node["votes"] = 0

#         self.graph.create(node)
    
#     async def create_role(self, role_name: str, role_id: int):
#         node = Node("Role")
#         node["name"] = role_name
#         node["role_id"] = role_id
        
#         self.graph.create(node)
    
#     async def connect_user_to_role(self, discord_id: int, role_id: int):
#         user_node = self.graph.find("User", "discord_id", discord_id)
#         role_node = self.graph.find("Role", "role_id", role_id)
#         relationship = Relationship(user_node, "HAS", role_node)
#         self.graph.create(relationship)


