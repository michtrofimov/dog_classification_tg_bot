from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from pydantic import SecretStr
from redis.asyncio import ConnectionPool, Redis

from photo_enhancer_tg_bot.core.config import bot_config

token: SecretStr = bot_config.bot.token

bot = Bot(token=token)

redis_client = Redis(
    connection_pool=ConnectionPool(
        host=bot_config.cache.host,
        port=bot_config.cache.port,
        password=bot_config.cache.password,
        db=bot_config.cache.db,
    ),
)

storage = RedisStorage(
    redis=redis_client,
    key_builder=DefaultKeyBuilder(with_bot_id=True),
)

dp = Dispatcher(storage=storage)
