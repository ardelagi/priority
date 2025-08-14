
import os
from motor.motor_asyncio import AsyncIOMotorClient

_client = None
_db = None

async def connect_database():
    global _client, _db
    uri = os.getenv("MONGODB_URI")
    _client = AsyncIOMotorClient(uri)
    _db = _client.get_default_database()

async def close_database():
    global _client
    if _client:
        _client.close()

def get_db():
    if _db is None:
        raise RuntimeError("Database not connected. Call connect_database() first.")
    return _db
