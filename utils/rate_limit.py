
import time
from discord import app_commands

# Simple in-memory rate limiter per (user_id, command_name)
_LAST_CALL = {}

def rate_limit(seconds: int = 5):
    def predicate(interaction: discord.Interaction) -> bool:
        key = (interaction.user.id, interaction.command.name if interaction.command else "unknown")
        now = time.time()
        last = _LAST_CALL.get(key, 0)
        if now - last < seconds:
            raise app_commands.CheckFailure(f"You're on cooldown. Try again in {int(seconds - (now-last))}s")
        _LAST_CALL[key] = now
        return True
    return app_commands.check(predicate)
