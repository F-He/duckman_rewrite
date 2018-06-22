import yaml
from src.database import Database

class currencySystem(object):
    def __init__(self, database: Database):
        self._database = database
        self._valueContainer = {}