import discord
import json

class RoleManager():
    def __init__(self, bot):
        self._availableRoles = None
        self._bot = bot
        self._embedgenerator = None

        with open("./cfg/roles.json", 'r', encoding="utf-8") as stream:
            self._availableRoles = json.load(stream)
    
    async def loadEmbedGenerator(self, embedgenerator):
        self._embedgenerator = embedgenerator

    async def getAvailableRoles(self):
        return self._availableRoles
    
    async def startRoleManagement(self, ctx, _roleMessage = None):
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
        await roleMessage.add_reaction("➕")
        await roleMessage.add_reaction("➖")
        await roleMessage.add_reaction("🚮")
        return roleMessage
    
    async def addRoleSection(self, ctx, roleMessage: discord.Message):
        pass
    
    async def removeRoleSection(self, ctx, roleMessage: discord.Message):
        await roleMessage.clear_reactions()
        await roleMessage.edit(embed=await self._embedgenerator.generateRemoveRoleEmbed(ctx.message.author))
        for emoji, rolename in self._availableRoles["languages"].items():
            role = discord.utils.get(ctx.message.author.roles, name=rolename)
            if role is not None:
                await roleMessage.add_reaction(emoji)
        await self.makeHomeAvailable(ctx, roleMessage)
    
    async def removeAllRoleSection(self, ctx, roleMessage: discord.Message):
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