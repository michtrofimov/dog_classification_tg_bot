import asyncio

from photo_enhancer_tg_bot.core.logger import AsyncLogger

"""Test the alert sending mechanism"""
# Execute with mock session
# Preferred way - use async context manager
async def main():
    alert_message = AsyncLogger.send_alert("Test")
    return await alert_message


asyncio.run(main())

# # Assertions
# assert "https://api.telegram.org/bot" in call_args["url"]
# assert "Test message" in call_args["json"]["text"]
# assert call_args["timeout"].total == 2
