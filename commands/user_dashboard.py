
import discord
from discord import app_commands
from discord.ext import commands
from ..models.subscription import Subscription

class UserDashboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="dashboard", description="Show your dashboard")
    async def dashboard(self, interaction: discord.Interaction):
        sub = await Subscription.get(interaction.user.id)
        status = "No active subscription" if not sub else "Active until: {}".format(sub.get("expires_at", "unknown"))
        embed = discord.Embed(title=f"{interaction.user.name}'s Dashboard")
        embed.add_field(name="Subscription", value=status, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(UserDashboard(bot))
