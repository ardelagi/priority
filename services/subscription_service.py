
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ..utils.database_connector import get_db

async def ensure_subscription(user_id: int, tier: str = "Gold", days: int = 30, license_key: str | None = None):
    db = get_db()
    now = datetime.utcnow()
    doc = await db.subscriptions.find_one({"user_id": user_id})
    if doc and doc.get("end_date"):
        start = max(now, doc["end_date"])
    else:
        start = now
    end = start + timedelta(days=days)
    await db.subscriptions.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "tier": tier,
            "start_date": start,
            "end_date": end,
            "license": license_key,
            "updated_at": now
        }},
        upsert=True
    )
    return end

async def get_active(query: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    db = get_db()
    now = datetime.utcnow()
    q = {"end_date": {"$gt": now}}
    if query:
        q.update(query)
    cursor = db.subscriptions.find(q)
    return [doc async for doc in cursor]

async def get_expiring_in(days: int) -> List[Dict[str, Any]]:
    db = get_db()
    now = datetime.utcnow()
    upper = now + timedelta(days=days)
    cursor = db.subscriptions.find({"end_date": {"$gte": now, "$lte": upper}})
    return [doc async for doc in cursor]

async def cleanup_expired() -> int:
    db = get_db()
    now = datetime.utcnow()
    res = await db.subscriptions.delete_many({"end_date": {"$lte": now}})
    return res.deleted_count

async def get_user_sub(user_id: int) -> Optional[Dict[str, Any]]:
    db = get_db()
    return await db.subscriptions.find_one({"user_id": user_id})
