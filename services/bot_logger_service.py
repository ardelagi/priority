
import logging

logger = logging.getLogger("prio-bot")
logger.setLevel(logging.INFO)
_handler = logging.StreamHandler()
_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
