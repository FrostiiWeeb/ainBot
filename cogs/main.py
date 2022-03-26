import discord
import subclass
from discord.ext import commands
class Main(commands.Cog):
    def __init__(self, bot:subclass.CustomBot):
        self.bot = bot


async def setup(bot:subclass.CustomBot):
    await bot.add_cog(Main(bot=bot))