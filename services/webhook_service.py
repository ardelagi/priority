
import aiohttp
from .bot_logger_service import logger

async def send_webhook(url: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, timeout=15) as resp:
                text = await resp.text()
                logger.info("Webhook POST %s -> %s", url, resp.status)
                if resp.status >= 400:
                    logger.error("Webhook error %s: %s", resp.status, text)
                return resp.status, text
        except Exception as e:
            logger.exception("Webhook failed: %s", e)
            return None, str(e)
