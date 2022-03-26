import discord
from discord.ext import commands


class ReportBug(discord.ui.View):
    def __init__(
        self, bot: commands.Bot, exception: Exception, message: discord.Message
    ):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="Join the Discord Server", url="https://discord.gg/FjfR6uDBgs"
            )
        )
        self.bot = bot
        self.error = exception
        self.message = message

    @discord.ui.button(
        label="Report Bug",
        style=discord.ButtonStyle.gray,
        emoji=discord.PartialEmoji(name="🐝"),
    )
    async def reportbug(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.message.author.id:
            await interaction.response.send_message(
                "You can't use this button.", ephemeral=True
            )
        else:
            channel = self.bot.get_channel(957156087063257098)
            emb = discord.Embed(
                title="An error occurred!",
                description=f"In guild {self.message.guild.id}, channel {self.message.channel.mention}, with message ID {self.message.id} at {self.message.created_at}. ```{self.error}```",
            )
            await channel.send(embed=emb)
            await interaction.response.send_message(
                "Successfully reported bug.", ephemeral=True
            )
            button.disabled = True
            await interaction.message.edit(view=self)
