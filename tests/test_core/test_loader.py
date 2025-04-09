from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from photo_enhancer_tg_bot.core.loader import bot, dp, redis_client, storage


class TestLoader:
    @pytest.fixture(autouse=True)
    def _setup_mocks(self):
        """Patch external dependencies"""
        with patch("aiogram.Bot") as self.mock_bot, patch(
            "redis.asyncio.Redis"
        ) as self.mock_redis, patch(
            "aiogram.fsm.storage.redis.RedisStorage"
        ) as self.mock_storage:
            yield

    def test_bot_initialization(self):
        """Verify bot is created with correct token"""
        from photo_enhancer_tg_bot.core.loader import bot

        assert isinstance(bot, MagicMock)
        self.mock_bot.assert_called_once_with(
            token=bot_config.bot.token.get_secret_value(), parse_mode=ParseMode.HTML
        )

    def test_redis_connection(self):
        """Test Redis connection pool setup"""
        from photo_enhancer_tg_bot.core.loader import redis_client

        self.mock_redis.assert_called_once_with(
            connection_pool=ConnectionPool(
                host=bot_config.cache.host,
                port=bot_config.cache.port,
                password=bot_config.cache.password,
                db=bot_config.cache.db,
            )
        )

    @pytest.mark.asyncio
    async def test_storage_initialization(self):
        """Verify storage uses correct Redis client and key builder"""
        from photo_enhancer_tg_bot.core.loader import storage

        self.mock_storage.assert_called_once_with(
            redis=redis_client, key_builder=DefaultKeyBuilder(with_bot_id=True)
        )
        assert await storage.redis.ping()  # Test connection

    def test_dispatcher_setup(self):
        """Check dispatcher uses correct storage"""
        from photo_enhancer_tg_bot.core.loader import dp

        assert dp.storage == storage
