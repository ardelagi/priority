
import discord
from ..services.subscription_service import ensure_subscription
from ..services.bot_logger_service import logger

async def handle_modal(interaction: discord.Interaction):
    cid = interaction.data.get("custom_id")
    comps = interaction.data.get("components", [])
    fields = {}
    # Flatten modal fields
    for row in comps:
        for comp in row.get("components", []):
            fields[comp.get("custom_id")] = comp.get("value")

    if cid == "add_member_modal":
        try:
            user_id = int(fields.get("userId"))
            tier = fields.get("tier", "Gold")
            days = int(fields.get("duration", "30"))
            license_key = fields.get("license") or None
            end = await ensure_subscription(user_id, tier=tier, days=days, license_key=license_key)
            await interaction.response.send_message(f"Added/extended sub for <@{user_id}> until {end:%Y-%m-%d}.", ephemeral=True)
        except Exception as e:
            logger.exception("add_member_modal error: %s", e)
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
    elif cid == "bulk_extend_modal":
        tier = fields.get("tier") or None
        days = int(fields.get("days", "0"))
        await interaction.response.send_message(f"Bulk extend by {days} days for tier='{tier or 'All'}' (placeholder).", ephemeral=True)
    else:
        await interaction.response.send_message("Unknown modal.", ephemeral=True)
