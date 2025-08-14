
from ..services.bot_logger_service import logger

def log_action(action: str):
    logger.info("[ADMIN] %s", action)
