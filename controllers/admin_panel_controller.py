
import discord
from discord import app_commands
from discord.ext import commands
from .helpers import log_action
from .stats_controller import get_stats

class AdminPanel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="admin_panel", description="Open admin panel")
    @app_commands.default_permissions(administrator=True)
    async def admin_panel(self, interaction: discord.Interaction):
        stats = await get_stats()
        embed = discord.Embed(title="Admin Panel")
        embed.add_field(name="Total logs", value=str(stats["total"]), inline=True)
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Quick Stats", custom_id="quick_stats"))
        view.add_item(discord.ui.Button(label="Refresh", custom_id="refresh_panel"))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup_admin_panel(bot: commands.Bot):
    # Admin panel is a Cog so slash command gets registered
    bot.add_cog = bot.add_cog  # no-op, cog is loaded via commands loader if needed
