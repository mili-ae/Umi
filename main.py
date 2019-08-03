import asyncio
import datetime
import json
import logging
import os
import random
import traceback

import discord
from discord.ext import commands, tasks


def get_prefix(bot, message):
    prefixes = bot.config["prefixes"]
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix)

with open("./data/config.json") as f:
    bot.config = json.load(f)
    

bot.loaded_cogs = list()
bot.color = 0x78DBE2
bot.launch_time = datetime.datetime.utcnow()
debug_mode = bot.config["debug_mode"]

#setting up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("discord.log", "w", "utf-8")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


if __name__ == "__main__":
    if debug_mode == True:
        bot.load_extension("cogs.owner")
        bot.loaded_cogs.append("owner")
        bot.load_extension("cogs.errorhandler")
        bot.loaded_cogs.append("errorhandler")
    else:
        for cog in os.listdir("./cogs"):
            try:
                if cog.endswith(".py") and cog not in bot.config["ignored_cogs"]:
                    bot.load_extension("cogs." + cog.replace(".py", ""))
                    bot.loaded_cogs.append(cog.replace(".py", ""))
            except:
                print(traceback.print_exc())
                continue


@bot.event
async def on_ready():
    print("Bot online and ready to work!")
    print("-----------------------------")
    print("Running on Python 3.6.5")
    print(f"discord.py ver: {discord.__version__}")
    print(f"Mode: {'DEV Debug' if debug_mode else 'Release'}")
    print("-----------------------------")
    print("Made by Løwenn#8437 with love <3")

      
bot.run(bot.config["token"])
