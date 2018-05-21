import pymongo
from src.secrets import MONGO_DB_KEY

class Database(object):
    def __init__(self, mongo_db_key):
        self._client = pymongo.MongoClient(mongo_db_key)
        self._user_base = self._client.discord_db.users
    
    async def create_new_user(self, user_id: int, user_name):
        try:
            post = {
                "_id": user_id,
                "user_name": user_name,
                "xp": 0,
                "gamble_won": 0,
                "gamble_lost": 0,
                "myrole": None,
                "helper_votes": 0,
                "last_vote": None
            }
            post_id = self._user_base.insert_one(post).inserted_id
            return post_id
        except:
            return None
    
    async def find_user(self, user_id: int):
        try:
            print(self._user_base.full_name)
            found = self._user_base.find_one({"_id": user_id})
            print(found)
            return found
        except:
            return None
    
    async def update_user(self, user_id:int, change_dict: dict):
        try:
            update = self._user_base.update_one(
                {"_id": user_id}, 
                {"$set": change_dict}
                )
            return update
        except:
            return None
    
    async def get_all(self):
        try:
            data = self._user_base.find()
            r_data = {}
            for d in data:
                r_data[d["_id"]] = d
            return r_data
        except:
            return None
    
    async def get_user_xp(self, user_id: int):
        try:
            data = await self.find_user(user_id)
            return data["xp"]
        except Exception as e:
            print(e)
            return None