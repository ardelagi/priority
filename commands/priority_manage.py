
import discord
from discord import app_commands
from discord.ext import commands
from ..controllers.priority_controller import log_priority_change
from ..models.priority_log import PriorityLog
from ..services.subscription_service import get_user_sub, ensure_subscription, get_active, get_expiring_in
from ..utils.pagination import paginate
from ..utils.rate_limit import rate_limit

class Priority(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    group = app_commands.Group(name="priority", description="Priority management")

    @group.command(name="add", description="Add priority subscription for a user")
    @app_commands.describe(user="Target user", tier="Tier name", days="Duration in days", license="License key (optional)")
    @app_commands.checks.has_permissions(administrator=True)
    async def add(self, interaction: discord.Interaction, user: discord.User, tier: str, days: int, license: str | None = None):
        end = await ensure_subscription(user.id, tier=tier, days=days, license_key=license)
        await log_priority_change(user.id, {"action": "add", "tier": tier, "days": days, "by": interaction.user.id})
        await interaction.response.send_message(f"Priority added for {user.mention} until {end:%Y-%m-%d}.", ephemeral=True)

    @group.command(name="renew", description="Renew priority for a user")
    @app_commands.describe(user="Target user", days="Add days")
    @app_commands.checks.has_permissions(administrator=True)
    async def renew(self, interaction: discord.Interaction, user: discord.User, days: int):
        sub = await get_user_sub(user.id)
        end = await ensure_subscription(user.id, tier=sub.get("tier","Gold") if sub else "Gold", days=days, license_key=sub.get("license") if sub else None)
        await log_priority_change(user.id, {"action": "renew", "days": days, "by": interaction.user.id})
        await interaction.response.send_message(f"Renewed {user.mention} until {end:%Y-%m-%d}.", ephemeral=True)

    @group.command(name="remove", description="Remove priority (set to expired)")
    @app_commands.describe(user="Target user")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove(self, interaction: discord.Interaction, user: discord.User):
        from ..utils.database_connector import get_db
        from datetime import datetime
        await get_db().subscriptions.update_one({"user_id": str(user.id)}, {"$set": {"end_date": datetime.utcnow()}})
        await log_priority_change(user.id, {"action": "remove", "by": interaction.user.id})
        await interaction.response.send_message(f"Removed priority for {user.mention}.", ephemeral=True)

    @group.command(name="check", description="Check user's priority")
    @app_commands.describe(user="Target user")
    async def check(self, interaction: discord.Interaction, user: discord.User | None = None):
        user = user or interaction.user
        from ..services.subscription_service import get_user_sub
        sub = await get_user_sub(user.id)
        if not sub:
            embed = discord.Embed(title="Active Priority").set_description(f"No active subscription for {user.mention}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed = discord.Embed(title="Active Priority")
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Tier", value=sub.get("tier","-"), inline=True)
        embed.add_field(name="Ends", value=str(sub.get("end_date","-")), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @group.command(name="list", description="List active priorities (paginated)")
    @app_commands.describe(page="Page number to show", per_page="Items per page")
    async def list(self, interaction: discord.Interaction, page: int = 1, per_page: int = 10):
        page = max(1, page)
        per_page = max(1, min(per_page,50))
        subs = await get_active()
        items, total = paginate(subs, page=page, per_page=per_page)
        lines = [f"• <@{s['user_id']}> — {s.get('tier','?')} until {s.get('end_date','?')}" for s in items]
        await interaction.response.send_message(f"Page {page} / {max(1, (total + per_page -1)//per_page)}\n" + ("\n".join(lines) or "No active subs."), ephemeral=True)

    @group.command(name="search", description="Search by tier or license")
    @app_commands.describe(query="Search term")
    async def search(self, interaction: discord.Interaction, query: str):
        from ..utils.database_connector import get_db
        db = get_db()
        docs = db.subscriptions.find({"$or": [{"tier": query}, {"license": query}]})
        docs = [d async for d in docs]
        lines = [f"• <@{d['user_id']}> — {d.get('tier','?')} ({d.get('license','-')})" for d in docs]
        await interaction.response.send_message("\n".join(lines) or "No matches.", ephemeral=True)

    @group.command(name="maintenance", description="Run maintenance tasks")
    @app_commands.checks.has_permissions(administrator=True)
    async def maintenance(self, interaction: discord.Interaction):
        from ..services.subscription_service import cleanup_expired
        deleted = await cleanup_expired()
        await interaction.response.send_message(f"Maintenance done. Deleted {deleted} expired records.", ephemeral=True)

async def setup(bot: commands.Bot):
    cog = Priority(bot)
    await bot.add_cog(cog)
    bot.tree.add_command(Priority.group)
