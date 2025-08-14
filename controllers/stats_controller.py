
from ..models.priority_log import PriorityLog

async def get_stats(limit: int = 50):
    logs = await PriorityLog.find_many(limit=limit)
    return {"total": len(logs), "latest": logs[:5]}
