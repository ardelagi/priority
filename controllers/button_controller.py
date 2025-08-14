
import discord
from ..services.bot_logger_service import logger
from ..services.subscription_service import get_expiring_in, cleanup_expired, get_active
from ..controllers.stats_controller import get_stats

async def handle_button(interaction: discord.Interaction):
    cid = interaction.data.get("custom_id")
    if cid == "quick_stats":
        stats = await get_stats()
        embed = discord.Embed(title="Quick Stats")
        embed.add_field(name="Total logs", value=str(stats["total"]), inline=True)
        await interaction.response.edit_message(embed=embed, view=None)
    elif cid == "expiring_today":
        subs = await get_expiring_in(0)
        lines = [f"<@{s['user_id']}> - {s.get('tier','?')}" for s in subs]
        msg = "\n".join(lines) or "No one expiring today."
        await interaction.response.send_message(msg, ephemeral=True)
    elif cid == "expiring_week":
        subs = await get_expiring_in(7)
        lines = [f"<@{s['user_id']}> - {s.get('tier','?')}" for s in subs]
        msg = "\n".join(lines) or "No one expiring this week."
        await interaction.response.send_message(msg, ephemeral=True)
    elif cid == "cleanup_now":
        deleted = await cleanup_expired()
        await interaction.response.send_message(f"Cleaned {deleted} expired records.", ephemeral=True)
    elif cid == "sync_roles":
        await interaction.response.send_message("Role sync placeholder done.", ephemeral=True)
    elif cid == "send_reminders":
        subs = await get_expiring_in(3)
        await interaction.response.send_message(f"Would send reminders to {len(subs)} users (placeholder).", ephemeral=True)
    elif cid == "backup_data":
        await interaction.response.send_message("Backup completed (placeholder).", ephemeral=True)
    elif cid == "system_health":
        active = await get_active()
        embed = discord.Embed(title="🏥 System Health Check")
        embed.add_field(name="Active subs", value=str(len(active)), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif cid == "add_member":
        modal = discord.ui.Modal(title="Add Member", custom_id="add_member_modal")
        modal.add_item(discord.ui.TextInput(label="User ID", custom_id="userId", required=True))
        modal.add_item(discord.ui.TextInput(label="Tier", custom_id="tier", required=True, placeholder="Gold/Silver/Bronze"))
        modal.add_item(discord.ui.TextInput(label="Duration (days)", custom_id="duration", required=True))
        modal.add_item(discord.ui.TextInput(label="License (optional)", custom_id="license", required=False))
        await interaction.response.send_modal(modal)
    elif cid == "bulk_extend":
        modal = discord.ui.Modal(title="Bulk Extend", custom_id="bulk_extend_modal")
        modal.add_item(discord.ui.TextInput(label="Tier filter", custom_id="tier", required=False, placeholder="Gold/All"))
        modal.add_item(discord.ui.TextInput(label="Days to extend", custom_id="days", required=True))
        modal.add_item(discord.ui.TextInput(label="Reason", custom_id="reason", required=False))
        await interaction.response.send_modal(modal)
    else:
        await interaction.response.send_message("Unknown button.", ephemeral=True)
        logger.warning("No handler for button id %s", cid)
