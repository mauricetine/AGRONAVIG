import redis
import json
import os
from typing import Optional, Any

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class CacheService:
    def __init__(self):
        try:
            self.redis = redis.from_url(REDIS_URL, decode_responses=True)
        except Exception as e:
            print(f"⚠️ Erreur connexion Redis : {e}")
            self.redis = None

    def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            return None
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: Any, expire: int = 3600):
        if not self.redis:
            return
        self.redis.set(key, json.dumps(value), ex=expire)

    def delete(self, key: str):
        if self.redis:
            self.redis.delete(key)

cache = CacheService()
