import yaml
from src.database import Database


class CurrencySystem(object):
    def __init__(self, database: Database):
        self._database = database
        self._valueContainer = {}

        self._valueContainer = self.loadCurrencyConfig("./cfg/currencyConfig.yml")
    

    def loadCurrencyConfig(self, path: str):
        with open(path, 'r', encoding="utf-8") as stream:
            return yaml.load(stream, Loader=yaml.Loader)
    

    async def getCurrencyValue(self, name: str):
        return self._valueContainer[name]
    

    async def addCoinsTo(self, user_id: int, coinsToAdd: int):
        await self._database.add_currency(user_id, coinsToAdd)
    

    async def getUserCoins(self, user_id: int):
        return await self._database.get_currency(user_id)
    
    
    async def setCurrency(self, user_id: int, newCurrencyAmount: int):
        await self._database.set_currency(user_id, newCurrencyAmount)