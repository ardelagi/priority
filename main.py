
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.environment_validator import validate_environment
from utils.database_connector import connect_database, close_database
from routes.commands import setup_commands
from services.reminder_service import setup_reminder_scheduler
from controllers.event_controller import setup_event_handlers
from controllers.error_controller import setup_error_handlers
from controllers.http_server import run_http_server
from services.bot_logger_service import logger

load_dotenv()
validate_environment()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
prefix = os.getenv("BOT_PREFIX", "!")

bot = commands.Bot(command_prefix=prefix, intents=intents)

async def startup():
    await connect_database()
    setup_reminder_scheduler(bot)
    setup_event_handlers(bot)
    setup_error_handlers(bot)
    await setup_commands(bot)

    http = asyncio.create_task(run_http_server())
    token = os.getenv("DISCORD_TOKEN")
    await bot.start(token)
    await http

def main():
    try:
        asyncio.run(startup())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(close_database())
        except Exception:
            pass

if __name__ == "__main__":
    main()
