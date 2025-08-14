
from typing import Dict, Any
from ..utils.database_connector import get_db

class Subscription:
    collection = lambda: get_db().subscriptions

    @classmethod
    async def get(cls, user_id: int):
        return await cls.collection().find_one({"user_id": user_id})
