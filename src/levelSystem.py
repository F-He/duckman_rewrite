import discord
import yaml
from src.database import Database
from src.embeds import EmbedGenerator


class LevelSystem():
    def __init__(self, db: Database, embedgen: EmbedGenerator):
        self._database = db
        self._embedgenerator = embedgen

        with open("./cfg/level.yml", 'r', encoding='utf-8') as stream:
            self.level_dict = yaml.load(stream, Loader=yaml.Loader)
    

    async def check_level(self, _user: discord.Member):
        user_xp = await self._database.get_user_xp(_user.id)
        user_level = await self._database.get_user_level(_user.id)

        for key, value in self.level_dict.items():
            if int(key) > user_level:
                if user_xp > value["xp"]:
                    await self._database.set_user_level(_user.id, int(key))
                    return await self._embedgenerator.generateLevelEmbed(_user, int(key), value)
        return None