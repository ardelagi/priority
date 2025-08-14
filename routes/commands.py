
import importlib
import pkgutil
from discord.ext import commands

async def setup_commands(bot: commands.Bot):
    # Auto-discover cogs in commands package
    import prio_main_python.commands as commands_pkg  # type: ignore
    for _, module_name, _ in pkgutil.iter_modules(commands_pkg.__path__):
        module_path = f"prio_main_python.commands.{module_name}"
        mod = importlib.import_module(module_path)
        if hasattr(mod, "setup"):
            await mod.setup(bot)
