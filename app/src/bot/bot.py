import asyncio

from app.src.loader import bot, BOT_TOKEN
from discord.ext.commands import Bot

from app.src.bot.commands.user.test import ping


async def build(app: Bot):
    app.remove_command('help')
    app.add_command(ping)
    await app.start(BOT_TOKEN)


def start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(build(bot))
