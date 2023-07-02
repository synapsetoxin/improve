from discord.ext.commands import Bot

from app.src.bot.commands.user import games
from app.src.bot.commands.user import help
from app.src.bot.commands.user import profile
from app.src.bot.commands.user import shop
from app.src.bot.commands.user import tournament


def add_commands(app: Bot):
    app.add_command(games.duel)
    app.add_command(help.report)
    app.add_command(profile.info)
    app.add_command(profile.dota)
    app.add_command(profile.transfer_money)
    app.add_command(shop.shop)
    app.add_command(tournament.reg)
    app.add_command(tournament.unreg)
