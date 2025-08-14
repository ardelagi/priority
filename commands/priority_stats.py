
import discord
from discord import app_commands
from discord.ext import commands
from ..controllers.stats_controller import get_stats

class PriorityStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="priority_stats", description="Show priority statistics")
    async def pr_stats(self, interaction: discord.Interaction):
        data = await get_stats(limit=50)
        embed = discord.Embed(title="Priority Stats")
        embed.add_field(name="Total logs", value=str(data["total"]), inline=True)
        embed.add_field(name="Latest shown", value=str(len(data["latest"])), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(PriorityStats(bot))
