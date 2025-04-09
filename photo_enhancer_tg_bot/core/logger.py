import aiohttp

from photo_enhancer_tg_bot.core.config import Settings


class AsyncLogger:
    @staticmethod
    async def send_alert(
        message: str,
    ) -> None:
        """Send alert with optional session injection for testing"""
        config = Settings()
        url = f"https://api.telegram.org/bot{config.logger.remote_token.get_secret_value()}/sendMessage"

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            # your code
            async with session.post(
                url, data={"chat_id": config.logger.alert_channel, "text": message}
            ) as response:
                await response.text()
