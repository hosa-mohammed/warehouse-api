import os
import json
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

async def init_cache(app):

    redis_url = os.getenv("REDIS_URL", "redis://warehouse_cache:6379/0")
    redis = aioredis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="warehouse-cache")

async def get_cached_products():

    cached_data, _ = await FastAPICache.get("all_products")
    
    if cached_data is not None:

        return json.loads(cached_data)
    
    return None