from discord.ext.commands import Bot

from app.src.bot.commands.admin import help
from app.src.bot.commands.admin import keep_it_closed
from app.src.bot.commands.admin import moderation
from app.src.bot.commands.admin import tournament


def add_commands(app: Bot):
    app.add_command(help.adminhelp)
    app.add_command(moderation.ban)
    app.add_command(moderation.gift)
    app.add_command(tournament.create_tournament)
    app.add_command(tournament.remove_tournament)
    app.add_command(tournament.cancel_tournament)
    app.add_command(tournament.reglist)
