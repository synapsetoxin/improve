from discord.ext.commands import Bot

from app.src.bot.events import tronscan


def all_events(app: Bot):
    app.event(tronscan.on_ready)
