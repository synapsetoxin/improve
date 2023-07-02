import asyncio

from discord.ext.commands import Bot

from app.src.loader import bot, BOT_TOKEN
from app.src.bot.commands import all_commands
from app.src.bot.events import all_events


async def build(app: Bot):
    app.remove_command('help')
    all_commands(app)
    all_events(app)
    await app.start(BOT_TOKEN)


def start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(build(bot))
