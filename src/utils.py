import time

from src.database import Database

voteCooldownInSeconds = 604800


class Utils():
    def __init__(self, db: Database):
        self._database = db
    
    async def userIsElegibleToVote(self, user_id: int):
        last_vote_time = await self._database.get_last_vote_time(user_id)
        if last_vote_time is not None:
            timeSinceLastVote = time.time() - last_vote_time
            if timeSinceLastVote >= voteCooldownInSeconds:
                return True
        else:
            return True
        return False
    
    async def generateWhoVotedMessage(self, user_id: int):
        allVoters = await self._database.getWhoVotedFor(user_id)
        if not allVoters:
            return "There are no Votes ¯\\_(ツ)_/¯"
        else:
            msg = "```\n"
            for voter in allVoters:
                msg += f"-{voter}\n"
            msg += "```"
            return msg