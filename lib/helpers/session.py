from lib.helpers.config import GetSettings
import aioredis

settings = GetSettings()


async def StorePair(key: str, value: str):
    redis = await aioredis.from_url(settings.REDIS_URL)
    await redis.set(key, value)
    await redis.close()


async def GetPair(key: str):
    redis = await aioredis.from_url(settings.REDIS_URL)
    pair = await redis.get(key)
    await redis.close()
    return pair