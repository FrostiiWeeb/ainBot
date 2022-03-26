import asyncio
import discord
import subclass
from discord.ext import commands

cdcooldown = []


class Fun(commands.Cog):
    def __init__(self, bot: subclass.CustomBot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    async def countdown(self, ctx: subclass.AinContext):
        for i in range(0, 3):
            await ctx.send(str(3 - i))
            await asyncio.sleep(1)
        await asyncio.sleep(1)
        await ctx.send("Done.")


async def setup(bot: subclass.CustomBot):
    await bot.add_cog(Fun(bot=bot))
