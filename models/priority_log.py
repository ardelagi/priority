
from typing import Optional, List, Any, Dict
from datetime import datetime
from ..utils.database_connector import get_db

class PriorityLog:
    collection = lambda: get_db().priority_logs

    @classmethod
    async def create(cls, data: Dict[str, Any]):
        data.setdefault("created_at", datetime.utcnow())
        res = await cls.collection().insert_one(data)
        return str(res.inserted_id)

    @classmethod
    async def find_many(cls, query: Dict[str, Any] = None, limit: int = 50):
        query = query or {}
        cursor = cls.collection().find(query).sort("created_at", -1).limit(limit)
        return [doc async for doc in cursor]
