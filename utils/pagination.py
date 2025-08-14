
from typing import List, Any

def paginate(items: List[Any], page: int = 1, per_page: int = 10):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], len(items)
