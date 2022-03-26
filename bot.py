import asyncio
import json
import discord
import asyncpg
import subclass

# Loading the config...
with open("config.json", "r") as f:
    config = json.load(f)

# Initializing the bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = subclass.CustomBot(command_prefix="a,", intents=intents)

cooldowns = []


@bot.event
async def on_ready():
    bot.owner_id = None
    bot.owner_ids = [745951784526282774, 857103603130302514, 554016618829709314]
    bot.con = await asyncpg.create_pool(
        user=config["postgres_user"],
        password=config["postgres_pass"],
        database=config["postgres_db"],
    )  # Starts the connection to PostgreSQL. Must be the FIRST thing the bot does.
    await bot.load_extension("jishaku")
    await bot.load_extension("cogs.fun")
    await bot.load_extension("cogs.admin")
    await bot.load_extension("cogs.main")

    print(f"Ready as {bot.user}!")


async def on_close():
    print("Goodbye.")
    with open("blacklisted.json", "r+") as f:
        json.dump(bot.blacklisted_ids, f)
    await bot.con.close()


# Opens the connection to Discord.
bot.run(config["token"])
# Makes sure the connection is closed before shutting down
asyncio.run(on_close())
