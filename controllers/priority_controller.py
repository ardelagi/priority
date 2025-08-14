
from ..models.priority_log import PriorityLog

async def log_priority_change(user_id: int, details: dict):
    await PriorityLog.create({"user_id": user_id, **details})
