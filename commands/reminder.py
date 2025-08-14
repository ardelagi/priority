
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from ..models.reminder import Reminder
from ..utils.rate_limit import rate_limit

class ReminderCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    group = app_commands.Group(name="reminder", description="Reminder utilities")

    @group.command(name="add", description="Add a reminder in N minutes")
    @app_commands.describe(minutes="Minutes from now", message="Reminder text")
    @rate_limit(10)
    async def add(self, interaction: discord.Interaction, minutes: int, message: str):
        minutes = max(1, min(minutes, 7*24*60))
        when = datetime.utcnow() + timedelta(minutes=minutes)
        await Reminder.upsert(interaction.user.id, when, message)
        await interaction.response.send_message(f"Okay {interaction.user.mention}, will remind in {minutes} minutes.", ephemeral=True)

    @group.command(name="list", description="List your reminders (paginated)")
    @app_commands.describe(page="Page number", per_page="Items per page")
    async def list(self, interaction: discord.Interaction, page: int = 1, per_page: int = 10):
        from ..utils.database_connector import get_db
        page = max(1, page)
        per_page = max(1, min(per_page,50))
        cursor = get_db().reminders.find({"user_id": interaction.user.id}).sort("when", 1)
        docs = [d async for d in cursor]
        from ..utils.pagination import paginate
        items, total = paginate(docs, page=page, per_page=per_page)
        lines = [f"• {d.get('when')} — {d.get('message')}" for d in items]
        await interaction.response.send_message(f"Page {page} / {max(1, (total + per_page -1)//per_page)}\n" + ("\n".join(lines) or "No reminders."), ephemeral=True)

    @group.command(name="remove", description="Remove reminders by text search")
    async def remove(self, interaction: discord.Interaction, contains: str):
        from ..utils.database_connector import get_db
        res = await get_db().reminders.delete_many({"user_id": interaction.user.id, "message": {"$regex": contains}})
        await interaction.response.send_message(f"Removed {res.deleted_count} reminders.", ephemeral=True)

    @group.command(name="test", description="Test reminder delivery (DM)")
    async def test(self, interaction: discord.Interaction):
        try:
            await interaction.user.send("Test reminder!")
            await interaction.response.send_message("Sent test DM.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Cannot DM you. Please open DMs.", ephemeral=True)

    @group.command(name="send-manual", description="Admin: send manual reminder to a user")
    @app_commands.checks.has_permissions(administrator=True)
    async def send_manual(self, interaction: discord.Interaction, user: discord.User, message: str):
        try:
            await user.send(message)
            await interaction.response.send_message("Sent.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("DM blocked.", ephemeral=True)

    @group.command(name="send-targeted", description="Admin: DM all expiring in N days")
    @app_commands.checks.has_permissions(administrator=True)
    async def send_targeted(self, interaction: discord.Interaction, days: int):
        from ..services.subscription_service import get_expiring_in
        subs = await get_expiring_in(days)
        sent = 0
        for s in subs:
            user = await self.bot.fetch_user(int(s["user_id"]))
            try:
                await user.send(f"Your subscription ({s.get('tier','?')}) expires on {s.get('end_date')}")
                sent += 1
            except Exception:
                pass
        await interaction.response.send_message(f"Sent {sent}/{len(subs)} DMs.", ephemeral=True)

async def setup(bot: commands.Bot):
    cog = ReminderCog(bot)
    await bot.add_cog(cog)
    bot.tree.add_command(ReminderCog.group)
