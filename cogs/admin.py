from re import A
import asyncpg
import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.con:asyncpg.Pool = bot.con

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(aliases=["r"])
    async def reload(self, ctx:commands.Context, extension:str):
        await self.bot.reload_extension(extension)
        emb = discord.Embed(title=":white_check_mark: Success!", description=f"Reloaded cog `{extension}`")
        await ctx.reply(embed=emb)

    @commands.command()
    async def errortest(self, ctx:commands.Context):
        raise Exception("This is a test.")

    @commands.command()
    async def blacklist(self, ctx:commands.Context, user:discord.User):
        self.bot.blacklisted_ids.append(user.id)
        await ctx.reply("Blacklisted.")
    
    @commands.command()
    async def unblacklist(self, ctx:commands.Context, user:discord.User):
        if not user.id in self.bot.blacklisted_ids:
            return await ctx.reply("That person isn't blacklisted.")
        self.bot.blacklisted_ids.remove(user.id)
        await ctx.reply("Unblacklisted.")
async def setup(bot):
    await bot.add_cog(Admin(bot))
