
import redis
import json
import hashlib
from typing import Optional, Any
from dotenv import load_dotenv
import os

load_dotenv()

class RedisCache:
    """Redis cache for search results and agent state"""
    
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD", None),
            decode_responses=True
        )
    
    def _make_key(self, prefix: str, query: str) -> str:
        """Generate cache key from query"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return f"{prefix}:{query_hash}"
    
    def get_search_results(self, query: str, source: str) -> Optional[list]:
        """Retrieve cached search results"""
        key = self._make_key(f"search:{source}", query)
        cached = self.client.get(key)
        
        if cached:
            return json.loads(cached)
        return None
    
    def cache_search_results(self, query: str, source: str, results: list, ttl: int = 86400):
        """
        Cache search results
        ttl: Time to live in seconds (default 24 hours)
        """
        key = self._make_key(f"search:{source}", query)
        self.client.setex(key, ttl, json.dumps(results))
    
    def get_subsystem_state(self, subsystem: str) -> Optional[dict]:
        """Get cached TRL assessment state for subsystem"""
        key = f"state:marvel:{subsystem}"
        cached = self.client.get(key)
        
        if cached:
            return json.loads(cached)
        return None
    
    def save_subsystem_state(self, subsystem: str, state: dict):
        """Save TRL assessment state"""
        key = f"state:marvel:{subsystem}"
        self.client.set(key, json.dumps(state))
    
    def clear_cache(self, pattern: str = "*"):
        """Clear cache by pattern"""
        for key in self.client.scan_iter(pattern):
            self.client.delete(key)