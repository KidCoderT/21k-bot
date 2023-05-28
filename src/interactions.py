import discord
from discord.ui.item import Item
from .people import Peeps


class LoginModel(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            title="Login Model",
        )
        self.add_item(
            discord.ui.InputText(
                label="Email", placeholder="School Email", required=True
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Password", placeholder="School Password", required=True
            )
        )

    async def callback(self, interaction: discord.Interaction):
        if Peeps.fetch(interaction.user.id) is not None:
            return await interaction.response.send_message(
                "You have already been logged in 😑"
            )

        await interaction.response.defer(ephemeral=True)

        worked = Peeps.new(
            interaction.user.id,
            *[child.value for child in self.children],  # type: ignore
        )

        if worked:
            return await interaction.followup.send("Logged in Successfully ✅")

        await interaction.followup.send("Failed to Login Invalid Creds")
