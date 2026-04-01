import redis
import json
from typing import Any, Dict, Optional

class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def save_chat(self, session_id: str, chat_data: Dict[str, Any]):
        """Save chat data to Redis."""
        key = f"chat:{session_id}"
        self.client.rpush(key, json.dumps(chat_data))
        self.client.expire(key, 86400)  
        
    def get_chat(self, session_id: str) -> list[Any]:
        key = f"chat:{session_id}"
        history = self.client.lrange(key, 0, -1)
        return [json.loads(m) for m in history]
    
    def clear_chat(self, session_id: str):
        key = f"chat:{session_id}"
        self.client.delete(key)

    
