
from ..services.bot_logger_service import logger

def setup_error_handlers(bot):
    @bot.event
    async def on_command_error(ctx, error):
        logger.exception("Command error: %s", error)
        await ctx.send(f"Error: {error}")
