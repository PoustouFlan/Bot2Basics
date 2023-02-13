import discord
import asyncio
from bot_utils import *
from discord.ext import commands

import logging
log = logging.getLogger("Bot2Basics")
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
log.addHandler(stream)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix = "$ ",
    help_command = None,
    intents = intents
)

initial_extensions = [
]

@bot.event
async def on_ready():
    log.info(f"Connecté en tant que {bot.user}")


async def load():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            log.info(f"{extension} chargée avec succès")
        except Exception as e:
            log.error(f"Échec du chargement de {extension}")
            log.error(e)


async def main():
    await load()

    await bot.start(TOKEN)

asyncio.run(main())