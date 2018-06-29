import discord
import json
from src.database import Database
from src.embeds import EmbedGenerator


class LevelSystem():
    def __init__(self, db: Database, embedgen: EmbedGenerator, bot):
        self._database = db
        self._embedgenerator = embedgen
        self._bot = bot

        with open("./cfg/level.json", 'r') as stream:
            self.level_dict = json.load(stream)
    

    async def check_level(self, _message: discord.Message):
        _user = _message.author
        user_xp = await self._database.get_user_xp(_user.id)
        user_level = await self._database.get_user_level(_user.id)

        for key, value in self.level_dict.items():
            if int(key) > user_level:
                if user_xp > value["xp"]:
                    await self._database.set_user_level(_user.id, int(key))
                    await self._check_rewards(int(key), _message)
                    await self._database.add_currency(_user.id, value["coins"])
                    return await self._embedgenerator.generateLevelEmbed(_user, int(key), value)
        return None
    
    async def set_user_level(self, user_id: int, level: int):
        await self._database.set_user_level(user_id, level)

    async def get_user_level(self, user_id: int):
        return await self._database.get_user_level(user_id)
    
    async def addXpTo(self, user_id: int, xp_to_add: int):
        await self._database.add_to_user_xp(user_id, xp_to_add)
    
    async def getXpFrom(self, user_id: int):
        return await self._database.get_user_xp(user_id)
    
    async def _check_rewards(self, level: int, message: discord.Message):
        if level == 5:
            await message.author.add_roles(discord.utils.get(message.guild.roles, name="Active 🦄"))