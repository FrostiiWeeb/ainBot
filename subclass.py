import time
import discord
from discord.ext import commands
from datetime import datetime
import views
import json


class Embed(discord.Embed):
    def __init__(
        self,
        *,
        color: int = 0x0307FC,
        title: str = "",
        description: str = "",
        type: str = "rich",
    ):
        super().__init__(colour=color, title=title, description=description, type=type)


# The context subclass
class AinContext(commands.Context):
    async def reply(self, content: str = None, **kwargs) -> discord.Message:
        if not "mention_author" in kwargs:  # Defaults mention_author to False.
            kwargs["mention_author"] = False
        if (
            not "override_color" in kwargs
        ):  # If we shouldn't override the default embed color, then don't override it.
            if (
                "embed" in kwargs
                and isinstance(kwargs["embed"], discord.Embed)
                and not "no_embed_override" in kwargs
            ):
                now = datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")
                kwargs["embed"].color = 0x0307FC
                kwargs["embed"].set_footer(
                    icon_url=self.author.avatar.url,
                    text=f"Requested by {self.author} at {now}",
                )
        return await super().reply(content, **kwargs)


# The bot subclass
class CustomBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("blacklisted.json", "r") as f:
            self.blacklisted_ids: list = json.load(f)

    async def on_command_error(
        self, ctx: commands.Context, exception: Exception, /
    ) -> None:
        emb = discord.Embed(title="Error!", description="")
        if isinstance(exception, commands.errors.CommandNotFound):
            emb.description = ":x: **No command with that name exists.**"
        elif isinstance(exception, commands.errors.CommandOnCooldown):
            emb.description = ":timer: **That command is on cooldown.**"
        elif isinstance(exception, commands.errors.BadArgument) or isinstance(
            exception, commands.errors.ArgumentParsingError
        ):
            emb.description = ":x: **Invalid argument.**"
        elif isinstance(exception, commands.errors.NotOwner):
            emb.description = ":x: **You aren't the owner of this bot.**"
        elif isinstance(exception, commands.errors.TooManyArguments):
            emb.description = ":x: **Too many arguments.**"
        elif isinstance(exception, commands.errors.MissingRequiredArgument):
            emb.description = f":x: **You are missing an argument: `{exception}`**"
        elif isinstance(exception, commands.errors.MaxConcurrencyReached):
            emb.description = ":x: **Too many people are using this command.**"
        else:
            emb.title = "That's not right..."
            emb.description = f":x: **An unknown error occurred! If you believe this is a bug, please click the button below to report it.** ```{exception}```"
            return await ctx.reply(
                embed=emb, view=views.ReportBug(self, exception, ctx.message)
            )
        await ctx.reply(embed=emb)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or AinContext)

    async def process_commands(self, message: discord.Message, /) -> None:
        if message.author.id in self.blacklisted_ids:
            view = discord.ui.View()
            view.add_item(
                discord.ui.Button(label="Appeal", url="https://discord.gg/FjfR6uDBgs")
            )
            emb = discord.Embed(
                title="Well..",
                description=":x: **You can't use ainBot because you're blacklisted. You can appeal by joining the discord server with the button below.**",
                color=0x000000,
            )
            return await message.channel.send(embed=emb, view=view)
        return await super().process_commands(message)
