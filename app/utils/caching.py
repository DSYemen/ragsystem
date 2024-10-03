from functools import lru_cache
from app.config import settings

@lru_cache(maxsize=100)
def cache_query_result(query: str):
    # هذه الدالة يمكن استخدامها لتخزين نتائج الاستعلامات المتكررة
    pass