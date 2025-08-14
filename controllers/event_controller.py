from services.bot_logger_service import logger
from .button_controller import handle_button
from .modal_controller import handle_modal

def setup_event_handlers(bot):
    @bot.event
    async def on_ready():
        logger.info("Bot online as %s", bot.user)
        try:
            synced = await bot.tree.sync()
            logger.info("Synced %d application commands", len(synced))
        except Exception as e:
            logger.exception("Failed to sync commands: %s", e)

    @bot.event
    async def on_interaction(interaction):
        if interaction.type.name == "component":
            await handle_button(interaction)
        elif interaction.type.name == "modal_submit":
            await handle_modal(interaction)
