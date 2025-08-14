
from typing import Dict, Any
from datetime import datetime
from ..utils.database_connector import get_db

class Reminder:
    collection = lambda: get_db().reminders

    @classmethod
    async def upsert(cls, user_id: int, when: datetime, message: str):
        await cls.collection().update_one(
            {"user_id": user_id, "when": when},
            {"$set": {"user_id": user_id, "when": when, "message": message}},
            upsert=True
        )
