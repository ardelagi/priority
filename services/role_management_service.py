
from .bot_logger_service import logger

async def add_role(member, role_name: str):
    role = next((r for r in member.guild.roles if r.name == role_name), None)
    if role:
        await member.add_roles(role, reason="Role management service")
        logger.info("Added role %s to %s", role_name, member)
        return True
    return False
