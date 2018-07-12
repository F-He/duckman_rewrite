import discord
import json

class RoleManager():
    def __init__(self, bot):
        self._availableRoles = None
        self._bot = bot
        self._embedgenerator = None
        self._currentState = {}

        with open("./cfg/roles.json", 'r', encoding="utf-8") as stream:
            self._availableRoles = json.load(stream)
    
    async def loadEmbedGenerator(self, embedgenerator):
        self._embedgenerator = embedgenerator

    async def getAvailableRoles(self):
        return self._availableRoles
    
    async def startRoleManagement(self, ctx, _roleMessage = None):
        self._currentState[ctx.message.author.id] = {}
        roleMessage = await self.mainRoleSection(ctx, _roleMessage)

        def check(reaction, user):
            return user == ctx.message.author and reaction.message.id == roleMessage.id
        reaction, user = await self._bot.wait_for("reaction_add", check=check)

        if str(reaction.emoji) == '➕':
            await self.addRoleSection(ctx, roleMessage)
        if str(reaction.emoji) == '➖':
            await self.removeRoleSection(ctx, roleMessage)
        if str(reaction.emoji) == '🚮':
            await self.removeAllRoleSection(ctx, roleMessage)

    async def mainRoleSection(self, ctx, roleMessage = None):
        if roleMessage is None:
            roleMessage = await ctx.send(embed=await self._embedgenerator.generateRoleEmbed(ctx.message.author))
        else:
            await roleMessage.clear_reactions()
            await roleMessage.edit(embed=await self._embedgenerator.generateRoleEmbed(ctx.message.author))
        self._currentState[ctx.message.author.id]["state"] = "home"
        self._currentState[ctx.message.author.id]["msgid"] = roleMessage.id
        await roleMessage.add_reaction("➕")
        await roleMessage.add_reaction("➖")
        await roleMessage.add_reaction("🚮")
        return roleMessage
    
    async def addRoleSection(self, ctx, roleMessage: discord.Message):
        self._currentState[ctx.message.author.id]["state"] = "add"
        self._currentState[ctx.message.author.id]["msgid"] = roleMessage.id
        await roleMessage.clear_reactions()
        await roleMessage.edit(embed=await self._embedgenerator.generateAddRoleEmbed(ctx.message.author))
        for emoji, rolename in self._availableRoles["languages"].items():
            role = discord.utils.get(ctx.message.author.roles, name=rolename)
            if role not in ctx.message.author.roles:
                await roleMessage.add_reaction(emoji)
        for emoji, rolename in self._availableRoles["other"].items():
            role = discord.utils.get(ctx.message.author.roles, name=rolename)
            if role not in ctx.message.author.roles:
                await roleMessage.add_reaction(emoji)
        await self.makeHomeAvailable(ctx, roleMessage)
    
    async def removeRoleSection(self, ctx, roleMessage: discord.Message):
        self._currentState[ctx.message.author.id]["state"] = "remove"
        self._currentState[ctx.message.author.id]["msgid"] = roleMessage.id
        await roleMessage.clear_reactions()
        await roleMessage.edit(embed=await self._embedgenerator.generateRemoveRoleEmbed(ctx.message.author))
        for emoji, rolename in self._availableRoles["languages"].items():
            role = discord.utils.get(ctx.message.author.roles, name=rolename)
            if role is not None:
                await roleMessage.add_reaction(emoji)
        for emoji, rolename in self._availableRoles["other"].items():
            role = discord.utils.get(ctx.message.author.roles, name=rolename)
            if role is not None:
                await roleMessage.add_reaction(emoji)
        await self.makeHomeAvailable(ctx, roleMessage)
    
    async def removeAllRoleSection(self, ctx, roleMessage: discord.Message):
        self._currentState[ctx.message.author.id]["state"] = "removeall"
        self._currentState[ctx.message.author.id]["msgid"] = roleMessage.id
        for emoji, rolename in self._availableRoles["languages"].items():
            role = discord.utils.get(ctx.message.author.roles, name=rolename)
            if role is not None:
                await ctx.message.author.remove_roles(role)
        for emoji, rolename in self._availableRoles["other"].items():
            role = discord.utils.get(ctx.message.author.roles, name=rolename)
            if role is not None:
                await ctx.message.author.remove_roles(role)
        await roleMessage.clear_reactions()
        await roleMessage.edit(embed=await self._embedgenerator.generateRemoveAllRolesEmbed(ctx.message.author))
        await self.makeHomeAvailable(ctx, roleMessage)
    
    async def makeHomeAvailable(self, ctx, roleMessage: discord.Message):
        await roleMessage.add_reaction("🏠")
        def check(reaction, user):
            return user == ctx.message.author
        reaction, user = await self._bot.wait_for("reaction_add", check=check)
        if str(reaction.emoji) == '🏠':
            await self.startRoleManagement(ctx, roleMessage)

    async def handleReactions(self, reaction, user):
        if user.id in self._currentState:
            if reaction.message.id == self._currentState[user.id]["msgid"]:
                if self._currentState[user.id]["state"] == "home":
                    return
                if self._currentState[user.id]["state"] == "add":
                    await self.handleAddState(reaction, user)
                if self._currentState[user.id]["state"] == "remove":
                    await self.handleRemoveState(reaction, user)
                if self._currentState[user.id]["state"] == "removeall":
                    await self.handleRemoveAllState(reaction, user)
    
    async def handleAddState(self, reaction, user):
        try:
            rolename = self._availableRoles["languages"][reaction.emoji]
            role = discord.utils.get(reaction.message.guild.roles, name=rolename)
            await user.add_roles(role)
            await reaction.message.channel.send(f"Added {rolename} to {user.name}")
        except:
            try:
                rolename = self._availableRoles["other"][reaction.emoji]
                role = discord.utils.get(reaction.message.guild.roles, name=rolename)
                await user.add_roles(role)
                await reaction.message.channel.send(f"Added {rolename} to {user.name}")
            except:
                pass
    
    async def handleRemoveState(self, reaction, user):
        try:
            rolename = self._availableRoles["languages"][reaction.emoji]
            role = discord.utils.get(user.roles, name=rolename)
            await user.remove_roles(role)
            await reaction.message.channel.send(f"Removed {rolename}")
        except:
            try:
                rolename = self._availableRoles["other"][reaction.emoji]
                role = discord.utils.get(user.roles, name=rolename)
                await user.remove_roles(role)
                await reaction.message.channel.send(f"Removed {rolename}")
            except:
                pass
    
    async def handleRemoveAllState(self, reaction, user):
        pass

        # {
        #     "9348910934134": {
        #         "state": "remove_roles",
        #         "msgid": "218971345753194"
        #     }
        # }


    def _editState(self, newState):
        self._currentState = newState

    def getState(self):
        return self._currentState