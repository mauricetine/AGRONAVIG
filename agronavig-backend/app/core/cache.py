import redis
import json
import os
from typing import Optional, Any

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class CacheService:
    def __init__(self):
        self._memory = {}
        try:
            self.redis = redis.from_url(REDIS_URL, decode_responses=True)
            self.redis.ping()
        except Exception as e:
            print(f"WARNING: Redis indisponible, cache mémoire activé : {e}")
            self.redis = None

    def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            return self._memory.get(key)
        try:
            data = self.redis.get(key)
            try:
                return json.loads(data) if data else None
            except (TypeError, json.JSONDecodeError):
                return data
        except Exception as e:
            print(f"WARNING: Lecture Redis impossible, cache mémoire utilisé : {e}")
            self.redis = None
            return self._memory.get(key)

    def set(self, key: str, value: Any, expire: int = 3600):
        self._memory[key] = value
        if not self.redis:
            return
        try:
            self.redis.set(key, json.dumps(value), ex=expire)
        except Exception as e:
            print(f"WARNING: Écriture Redis impossible, cache mémoire utilisé : {e}")
            self.redis = None

    def delete(self, key: str):
        self._memory.pop(key, None)
        if self.redis:
            try:
                self.redis.delete(key)
            except Exception as e:
                print(f"WARNING: Suppression Redis impossible : {e}")
                self.redis = None

cache = CacheService()
