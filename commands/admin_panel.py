
import discord
from discord.ext import commands
from discord import app_commands

class AdminPanel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="admin_panel", description="Priority Motionlife Admin Panel")
    @app_commands.default_permissions(administrator=True)
    async def admin_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Priority Motionlife Admin Panel")
        view = discord.ui.View()
        for label, cid in [
            ("Add Member","add_member"),
            ("Quick Stats","quick_stats"),
            ("Expiring Today","expiring_today"),
            ("Expiring Week","expiring_week"),
            ("Cleanup Now","cleanup_now"),
            ("Sync Roles","sync_roles"),
            ("Send Reminders","send_reminders"),
            ("Backup Data","backup_data"),
            ("System Health","system_health"),
            ("Bulk Extend","bulk_extend"),
        ]:
            view.add_item(discord.ui.Button(label=label, custom_id=cid))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminPanel(bot))
