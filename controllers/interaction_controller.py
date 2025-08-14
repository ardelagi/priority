
async def handle_interaction(interaction):
    await interaction.response.send_message("Interaction received.", ephemeral=True)
